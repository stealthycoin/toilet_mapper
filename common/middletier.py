import json
from django.core import serializers
from django.utils.timezone import utc
import datetime
import sys
from math import radians, sin, asin, cos, acos, atan, atan2, sqrt
from toilet.models import Toilet, Flag, FlagRanking
from review.models import Review

#turns post data into a json object
def post_to_dict(post):
    return remove_json_characters(dict(post))

#removes the json characters from the strings in the data from request
def remove_json_characters(dictionary):
    for elm in dictionary:
        dictionary[elm] = json.dumps(dictionary[elm]).replace("]","").replace("[","").replace("\"", "")
    return dictionary


#returns the time in a django timezone frinedly way
def currentTime():
   return  datetime.datetime.utcnow().replace(tzinfo=utc)


#serialize a thing(s)
def serialize(obj):
    return serializers.serialize('json', obj)
    

#adds error to beginning of response if required
def package_error(response, error):
    if error != '':
        return json.dumps({ 'error' : error })
    return response



#login stuff
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

#creates a new user
def create_user(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = request.POST
        try:
            User.objects.get(username=data['username'])#try to find someone with that name
            error = 'A user with that name already exists.'
            status = 200
        except ObjectDoesNotExist:#if it fails, we can create that user
            user = User.objects.create_user(data['username'],data['email'],data['password']) 
            user.save()
            response = '"' + data['username'] + ' created."'
    else:
        error += 'No POST data in request\n'
        status = 415
    return HttpResponse(package_error(response,error),status=status)


#logs in an existing user
def login(request):
    error = ''
    response = ''
    status = 200
    
    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'],password=data['password'])
        if user is not None:
            if user.is_active:
                django_login(request, user)
                response = '\"Success\"'
            else:
                error = 'Your account has been disabled\n'
        else:
            error += 'Invalid Login\n'
    else:
        error += 'No POST data in request.\n'
        status = 415
    return HttpResponse(package_error(response,error),status=status)


#its this simple
def logout(request):
    django_logout(request)
    response = '"Logged out"'

    return HttpResponse(package_error(response,''),status=200)


"""
COMMON OBJECT RETRIEVAL FUNCTIONS
"""

def str_to_class(str):
    lookup = {'Toilet': Toilet
              , 'Review': Review
              , 'FlagRanking': FlagRanking
              , 'Flag' : Flag}
    return lookup.get(str)

# We need to actually add in all of the large expesnive queries here        
def security_check(k, v):
    return v

#Distance between two (lat, long) coordinates
# Expects lat, long values in degrees
def distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
    
def get_obj(request, name):
    if request.POST:
        
        #get start and end for pagination 
        start = int(request.POST.get('start'))
        end = int(request.POST.get('end'))
        filters = json.loads(request.POST.get('filters'))
        #map over all of the filter objects to amke sure they aren't expensive queries
        filters = {k: security_check(k,v) for k, v in filters.items()}
        #convert the string from name into an object, apply all of the filters to the object
        qs = str_to_class(name).objects.all().filter(**filters)

        #Special case for sorting toilets by distance
        if request.POST.get('current_lat') != None:
            current_lat = float(request.POST.get('current_lat'))
            current_lng = float(request.POST.get('current_lng'))
            def distanceCmp(t1, t2):
                d1 = distance(current_lat, current_lng, t1.lat, t1.lng)
                d2 = distance(current_lat, current_lng, t2.lat, t2.lng)
                if d1 == d2: return 0
                return -1 if d1 < d2 else 1
            qs = list(qs)
            qs.sort(cmp=distanceCmp)

        return HttpResponse(serializers.serialize('json', qs[start:end]))

    else:
        return HttpResponse("DUDE WTF GIOMME A POST", status=412)
