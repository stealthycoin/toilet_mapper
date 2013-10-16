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
    
