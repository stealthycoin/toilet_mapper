from models import Toilet
import json
from common.middletier import post_to_dict, serialize, currentTime, package_error
from django.http import HttpResponse


#this adds a toilet using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = post_to_dict(request.POST)
        print request.user.is_authenticated()
        if not request.user.is_authenticated():
            status = 401
            error += 'Unauthorized creation of restroom. Please log in.\n'
        
        else:
            t = Toilet()
            data['date'] = currentTime()
            data['creator'] = request.user
            t.setattrs(data)
            t.save()

            response = serialize([t])
    else:
        error += 'No POST data in request.\n'
        status = 415

    return HttpResponse(package_error(response,error), status=status)



def listing(request):
    response = ''
    error = ''
    status = 201

    ts = Toilet.objects.all()
    response = seralize(ts)

    return HttpResponse(response,status=status)
