import json
from django.core import serializers
from django.utils.timezone import utc
import datetime

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
from django.contrib.auth import logout, authenticate
from django.http import HttpResponseg

def login(request):
    error = ''
    response = ''
    status = 200
    
    if request.method == 'POST':
        data = post_to_dict(request.POST)
        user = authenticate(username=data['username'],password=data['password'])
        if user is not None:
            if user.is_active:
                django_login(request, user)
                response = 'Success\n'
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
    logout(request)
    response = 'Logged out\n'
    return HttpResponse(package_error(response,''),status=200)
