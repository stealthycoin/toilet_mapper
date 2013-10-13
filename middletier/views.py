import datetime as datetime
import json
from django.db import models
from toilet.models import Toilet
from review.models import Review
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@login_required
def put (request):
    req_post_dict = request.POST
    model_attributes = remove_json_characters(dict(req_post_dict))
    response = ""
    status = 201
    update = False
    try: 
        if 'update' in req_post_dict and req_post_dict['update']:
            update = True 
        if req_post_dict['table'] == "toilet":
           if update:
              response = updateToilet(model_attributes, request)
           else:
              response = addToilet(model_attributes, request) 
        elif req_post_dict['table'] == "review":
            if update:
                response = updateReview(model_attributes)
            else:
                response = addReview(model_attributes, request)
           #No table specified
        else:
            status = 400
            response = "no table found"
    except KeyError as e:
        status = 400
        response = "Missing " + str(e).replace('\'',"") + " attribute" 
    except ValueError as e:
        status = 400
        response = str(e).replace('\'',"")
    except ObjectDoesNotExist as e:
        status = 404
        response = str(e).replace('\'',"")
    #201 for new resource created
    return HttpResponse(response,status=status)
        
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

def addToilet(model_attributes, request):
     t = Toilet()
     model_attributes['date'] = datetime.datetime.now()
     model_attributes['creator'] = request.user
     t.setattrs(model_attributes)
     t.save()
     return serializers.serialize('json', [t])

def updateToilet(model_attributes, request):
     #doesn't do anything at the moment because there is nothing to update
     t = Toilet.objects.get(pk = mode_attrbites['pk'])
     return serializers.serialize('json', [t])

def addReview(model_attributes, request):
    response = ""
    toilet_pk = model_attributes['toilet']
    model_attributes['toilet'] = Toilet.objects.get(pk=toilet_pk)
    model_attributes['user'] = request.user;
    model_attributes['date'] = datetime.datetime.now()
    #when writing new review, ranks should always start at zero
    model_attributes['rank'] = 0
    r = Review()
    r.setattrs(model_attributes)
    r.save()
    return serializers.serialize('json', [r]) 

def updateReview(model_attributes):
    response = ""
    pk = model_attributes['pk']
    newcontent = model_attributes['content']
    review = Review.objects.get(pk=pk)
    review.content = newcontent
    review.save()
    return serializers.serialize('json', [review])

#removes the json characters from the strings in the data from request
def remove_json_characters(dictionary):
    for elm in dictionary:
        dictionary[elm] = json.dumps(dictionary[elm]).replace("]","").replace("[","").replace("\"", "")
    return dictionary
