import json, datetime, sys
from django.core import serializers
from django.utils.timezone import utc
from math import radians, sin, asin, cos, acos, atan, atan2, sqrt
from toilet.models import Toilet, Flag, FlagRanking
from review.models import Review
from main.models import AdditionalUserInfo
from django.contrib.auth.models import check_password
from django.shortcuts import redirect

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
            userAdd = AdditionalUserInfo(user=user,\
                                         male=("1"==data['male']),\
                                         female=("1"==data['female']))
            userAdd.save()
            response = '"' + data['username'] + ' created."'
    else:
        error += 'No POST data in request\n'
        status = 415
    return HttpResponse(package_error(response,error),status=status)

#edit an existing user
#no catching because middleware should do that
def edit(request):
    error = ''
    response = ''
    status = 201
    
    data = request.POST

    if request.user.check_password(data['oldpassword']):
        u = request.user
        if request.user.username != data['username'] and len(User.objects.filter(username=data['username'])) > 0:
            return HttpResponse(json.dumps("Already taken"))
        u.username = data['username']
        if len(data['newpassword']) > 0:
            u.set_password(data['newpassword'])
        u.email = data['email']
        u.save()

        info = AdditionalUserInfo.objects.get(user=u)
        print data
        info.male = ("1" == data['male'])
        info.female = ("1" == data['female'])
        info.save()
    else:
        return HttpResponse(json.dumps("Wrong password"))

    return HttpResponse(json.dumps(data['username']))
    
        

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

# Distance between two (lat, long) coordinates
#  Expects lat, long values in degrees
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
        start = request.POST.get('start')
        if start != None: start = int(start)
        end = request.POST.get('end')
        if end != None: end = int(end)

        #sortby
        sortby = request.POST.get('sortby')

        filters = json.loads(request.POST.get('filters'))
        #map over all of the filter objects to amke sure they aren't expensive queries
        filters = {k: security_check(k,v) for k, v in filters.items()}
        #convert the string from name into an object, apply all of the filters to the object
        qs = str_to_class(name).objects.all().filter(**filters)
        #optional sorting
        if sortby: qs = qs.order_by(sortby)
        
        #Special case for sorting toilets by distance
        if request.POST.get('current_lat') != None:
            current_lat = float(request.POST.get('current_lat'))
            current_lng = float(request.POST.get('current_lng'))
            
            # These comparison functions use eachother to break ties
            #  which is why they pass an optional `final` argument.
            def distanceCmp(t1, t2, final=False):
                d1 = distance(current_lat, current_lng, t1.lat, t1.lng)
                d2 = distance(current_lat, current_lng, t2.lat, t2.lng)
                if d1 == d2: 
                    if(final == True): return 0
                    else: return ratingCmp(t1, t2, True);
                return -1 if d1 < d2 else 1
            def ratingCmp(t1, t2, final=False):
                if t1.rating == t2.rating: 
                    if(final == True): return 0
                    else: return distanceCmp(t1, t2, True);
                return -1 if t1.rating > t2.rating else 1

                qs = list(qs)
                if sortby == "-rating": qs.sort(cmp=ratingCmp)
                else: qs.sort(cmp=distanceCmp)
                    

        return HttpResponse(serializers.serialize('json', qs[start:end]))

    else:
        return HttpResponse("DUDE WTF GIOMME A POST", status=412)
