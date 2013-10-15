import json
from django.core import serializers
#turns post data into a json object
def post_to_dict(post):
    return remove_json_characters(dict(post))

#removes the json characters from the strings in the data from request
def remove_json_characters(dictionary):
    for elm in dictionary:
        dictionary[elm] = json.dumps(dictionary[elm]).replace("]","").replace("[","").replace("\"", "")
    return dictionary



#seralize a thing(s)
def seralize(obj):
    return serializers.serialize('json', [obj])
    
