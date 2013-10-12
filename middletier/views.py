import datetime as datetime
import json
from django.db import models
from toilet.models import Toilet
from review.models import Review
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def put (request):
    req_post_dict = request.POST
    model_attributes = remove_json_characters(dict(req_post_dict))
    repsponse = ""
    if (req_post_dict['table'] == "toilet"):
        t = Toilet()
        model_attributes['date'] = datetime.datetime.now()
        model_attributes['creator'] = request.user
        t.setattrs(model_attributes)
        t.save()
        response = serializers.serialize('json', [t])
    #the only field we need from the POST is the toliet id and the content 
    elif(req_post_dict['table'] == "review"):
        toilet_pk = model_attributes['toilet'][0]
        model_attributes['toilet'] = Toilet.objects.get(pk=toilet_pk)
        model_attributes['user'] = request.user;
        model_attributes['date'] = datetime.datetime.now()
        #when writing new review, ranks should always start at zero
        model_attributes['rank'] = 0
        r = Review()
        r.setattrs(model_attributes)
        r.save()
        response = serializers.serialize('json', [r])
    return HttpResponse(response)
        
def get (request):
    req_dict = request.GET
    filter_objects = {}
    if (req_dict['table'] == "toilet"):
        filter_objects = Toilet.objects 
        #table=toilet&pk=(/d+)
        if req_dict.__contains__('pk'):
            pk = req_dict['pk']
            filter_objects = filter_objects.filter(pk = pk)
        #table=toilet&user=(/d+) 
        if req_dict.__contains__('user'):
            user = req_dict['user']
        #elif google maps API shit for location, add during sprint 2
    elif  (req_dict['table'] == "review"):
        #table=review&toilet_id=(/d+)
        filter_objects = Review.objects
        if req_dict.__contains__('toilet_id'):
            toilet_id = req_dict['toilet_id']
            filter_objects = filter_objects.filter(toilet = toilet_id)
        if req_dict.__contains__('user'):
            user_id = req_dict['user']
            filter_objects = filter_objects.filter(user = user_id)
    response = serializers.serialize('json', filter_objects)
    return HttpResponse(response)

#removes the json characters from the strings in the data from request
def remove_json_characters(dictionary):
    for elm in dictionary:
        dictionary[elm] = json.dumps(dictionary[elm]).replace("]","").replace("[","").replace("\"", "")
    return dictionary
