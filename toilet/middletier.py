from models import Toilet
import json
from common.middletier import post_to_dict, serialize, currentTime
from django.http import HttpResponse


#this adds a toilet using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = post_to_dict(request.POST)
        t = Toilet()
        data['date'] = currentTime()
        data['creator'] = request.user
        t.setattrs(data)
        t.save()

        response = serialize([t])
                
    else:
        error += 'No POST data in request.\n'
        status = 415

    if error != '':
        response = error + '\n' + response


    return HttpResponse(response, status=status)
