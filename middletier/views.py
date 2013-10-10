from toilet.models import Toilet
from django.core import serializers
from django.http import HttpResponse

def get (request):
    req_dict = request.GET
    response = ""
    if (req_dict['table'] == "toilet"):
        pk = req_dict['pk']
        response = serializers.serialize('json', Toilet.objects.filter(pk = pk))
    return HttpResponse(response)