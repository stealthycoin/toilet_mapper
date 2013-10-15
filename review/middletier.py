from models import Review 
import json
from common.middletier import post_to_dict, seralize
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
        data['creator'] = request.user
        r.setattrs(data)
        r.save()

        response = seralize(t)
                
    else:
        error += 'No POST data in request.\n'
        status = 415

    if error != '':
        response = error + '\n' + response

    return HttpResponse(response, status=status)
