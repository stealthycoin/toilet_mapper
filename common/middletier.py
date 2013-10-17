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
        data = post_to_dict(request.POST)
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
        data = post_to_dict(request.POST)
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
