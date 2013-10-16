from models import Review
from toilet.models import Toilet
import json
from common.middletier import post_to_dict, serialize
from django.http import HttpResponse
import datetime

#this adds a review using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = post_to_dict(request.POST)
        r = Review()
        data['date'] = datetime.datetime.now()
        data['user'] = request.user
        data['toilet'] = Toilet.objects.get(pk=data['toilet'])
        r.setattrs(data)
        r.save()
        response = serialize([r])
    else:
        error += 'No POST data in request.\n'
        status = 415

    if error != '':
        response = error + '\n' + response

    return HttpResponse(response, status=status)



def get(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = post_to_dict()
        response = serialize(Review.objects.filter(toilet=data['toilet_id']))
    else:
        error += 'No POST data in request\n'
        status = 415

    if error != '':
        response = error + '\n' + response
    
    return HttpResponse(response,status=status)
    
