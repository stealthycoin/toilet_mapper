import datetime as datetime
from django.db import models
from toilet.models import Toilet
from review.models import Review
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def put (request):
    req_post_dict = request.POST
    if (req_post_dict['table'] == "toilet"):
        rqd = dict(req_post_dict)
        rqd['creator'] = request.user
        print "___________________________________________________________________"
        print request.user.pk
        rqd['date'] = datetime.datetime.now()
        t = Toilet()
        t.setattrs(rqd)
        t.save()
        return HttpResponse(t.pk)




def get (request):
    req_dict = request.GET
    response = ""
    if (req_dict['table'] == "toilet"):
        pk = req_dict['pk']
        response = serializers.serialize('json', Toilet.objects.filter(pk = pk))
    elif  (req_dict['table'] == "review"):
        toilet_id = req_dict['toilet_id']
        response = serializers.serialize('json', Review.objects.filter(toilet = toilet_id))
    return HttpResponse(response)
