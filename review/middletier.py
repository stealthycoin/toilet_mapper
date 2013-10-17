from models import Review
from toilet.models import Toilet
import json
from common.middletier import post_to_dict, serialize, currentTime, package_error
from django.http import HttpResponse


#this adds a review using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = post_to_dict(request.POST)
        r = Review()
        data['date'] = currentTime()
        data['user'] = request.user
        data['toilet'] = Toilet.objects.get(pk=data['toilet'])
        data['up_down_rank'] = 0;
        r.setattrs(data)
        r.save()
        response = serialize([r])
    else:
        error += 'No POST data in request.\n'
        status = 415

    return HttpResponse(package_error(response,error), status=status)


#thingies for getting reviews
def get(request):
    error = ''
    response = ''
    status = 200
    
    if request.method == 'POST':
        data = post_to_dict(request.POST)
        review_set = Review.objects.filter(toilet=data['toilet_id'])
        count = len(list(review_set))
        

        total = 0.0
        if count != 0:
            for review in review_set:
                total += review.rank

            total /= count
        else:
            total = -1

        review_set = review_set[int(data['start']):int(data['end'])] #cut out the part requested  wanted            
        d = {'count' : count, 'total' : total, 'review_set' : json.loads(serialize(review_set)) }
        response = json.dumps(d)

        
    else:
        error += 'No POST data in request\n'
        status = 415
        
    return HttpResponse(package_error(response,error),status=status)
    

#upvote downvote system
def upvote(request):
    error = ''
    status = 201
    if request.method == 'POST':
        data = post_to_dict(request.POST)
        r = Review.objects.get(pk=data['review_pk'])
        r.up_down_rank +=1
        r.setattrs(data)
        r.save()
        response = serialize([r])
    else:
        error += 'No POST data in request.\n'
        status = 415
    return HttpResponse(package_error(response,error), status=status)

def downvote(request):
    error = ''
    status = 201
    if request.method == 'POST':
        data = post_to_dict(request.POST)
        r = Review.objects.get(pk=data['review_pk'])
        r.up_down_rank -=1
        r.setattrs(data)
        r.save()
        response = serialize([r])
    else:
        error += 'No POST data in request.\n'
        status = 415
    return HttpResponse(package_error(response,error), status=status)
