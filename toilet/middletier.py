from models import Toilet
import json
from common.middletier import post_to_dict, seralize
from django.http import HttpResponse
import datetime

#this adds a toilet using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        print request.user
        data = post_to_dict(request.POST)
        t = Toilet()
        data['date'] = datetime.datetime.now()
        data['creator'] = request.user
        t.setattrs(data)
        t.save()

        response = seralize(t)
                
    else:
        error += 'No POST data in request.\n'
        status = 415

    if error != '':
        response = error + '\n' + response


    print response
    return HttpResponse(response, status=status)
