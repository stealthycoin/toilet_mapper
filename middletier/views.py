import datetime as datetime
import json
from django.db import models
from toilet.models import Toilet
from review.models import Review
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

class InvalidPostError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

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
    except InvalidPostError as e:
        status = 415
        response = e.value 
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
    try:
      status = 201
      req_dict = request.GET
      filter_objects = []
      if (req_dict['table'] == "toilet"):
          filter_objects = getToilet(req_dict)
      elif  (req_dict['table'] == "review"):
          filter_objects = getReview(req_dict)
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
    response = serializers.serialize('json', filter_objects)
    return HttpResponse(response,status =status)

def getReview(request):
     filter_objects = Review.objects.all()
     #table=review&toilet_id=(/d+)
     if request.__contains__('toilet_id'):
         toilet_id = request['toilet_id']
         filter_objects = filter_objects.filter(toilet = toilet_id)
     if request.__contains__('user'):
         user_id = request['user']
         filter_objects = filter_objects.filter(user = user_id)
     return filter_objects


def getToilet(request):
    filter_objects = Toilet.objects.all()
    #table=toilet&pk=(/d+)
    if request.__contains__('pk'):
        pk = request['pk']
        filter_objects = filter_objects.filter(pk = pk)
    #table=toilet&user=(/d+) 
    if request.__contains__('user'):
        user = request['user']
        filter_objects = filter_ojbects.filter(creator=user)
    #elif google maps API shit for location, add during sprint 2
    return filter_objects


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
    
    if len(Review.objects.filter(user=request.user,toilet=toilet_pk)) > 0:
       raise InvalidPostError("Cannot post multiple reviews for one restroom")

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
    review = Review.objects.get(pk=pk)
    noUpdate = True
    if 'content' in model_attributes:
        review.content = model_attributes['content'] 
        noUpdate = False
    if 'rank' in model_attributes: 
        review.rank = model_attributes['rank']
        noUpdate = False
    if noUpdate:
        raise KeyError("more than one")
    review.save()
    return serializers.serialize('json', [review])

#removes the json characters from the strings in the data from request
def remove_json_characters(dictionary):
    for elm in dictionary:
        dictionary[elm] = json.dumps(dictionary[elm]).replace("]","").replace("[","").replace("\"", "")
    return dictionary
