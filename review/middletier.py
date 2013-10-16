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
        data = post_to_dict(request.POST)
        review_set = Review.objects.filter(toilet=data['toilet_id'])
        count = len(list(review_set))

        total = 0.0
        for review in review_set:
            total += review.rank


        total /= count

        d = {'count' : count, 'total' : total, 'review_set' : json.loads(serialize(review_set)) }
        response = json.dumps(d)

        
    else:
        error += 'No POST data in request\n'
        status = 415
        
    if error != '':
        response = error + '\n' + response
 
    print response
    return HttpResponse(response,status=status)
    
