from models import Review, Vote
from toilet.models import Toilet
import json
from common.middletier import post_to_dict, serialize, currentTime, package_error
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db import transaction

#this adds a review using the post data
def add(request):
    error = ''
    response = ''
    status = 201
    if request.method == 'POST':
        data = request.POST.copy()        
        #We shouldn't be allowed to review a restroom twice
        if len(Review.objects.filter(user=request.user).filter(toilet=data['toilet'])) == 0:
            r = Review()
            with transaction.commit_on_success():
                toilet = Toilet.objects.get(pk=data['toilet'])                
                data['toilet'] = toilet
                toilet.updateRating(data['rank']) 
            data['date'] = currentTime()
            data['user'] = request.user
            data['up_down_rank'] = 0;
            r.setattrs(data)
            r.save()
            

            response = serialize([r])
        else:
            error += 'Cannot write more than one review.\n'
            status = 403
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
        print request
        data = request.POST
        review_set = Review.objects.filter(toilet=data['toilet_id'])
        count = len(list(review_set))
        
        total = 0.0
        if count != 0:
            for review in review_set:
                total += review.rank #need to change this

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
@transaction.commit_on_success
def vote(request, new_vote):
    response = ''
    error = ''
    status = 201
    if not request.user.is_authenticated():
        error = 'wtf bro log in'
    elif request.method == 'POST':
        data = request.POST
        r = Review.objects.get(pk=data['review_pk'])
        try:
            prev_vote_obj = Vote.objects.get(review=r.pk, user = request.user)
            prev_vote = prev_vote_obj.vote
            if new_vote != prev_vote:
                prev_vote_obj.delete()
                r.up_down_rank += new_vote
        except ObjectDoesNotExist:
            r.up_down_rank += new_vote
            v = Vote(user = request.user, review = r, vote = new_vote)
            v.save()
        r.save()
        response = serialize([r])
    else:
        error += 'No POST data in request.\n'
        status = 415
    return HttpResponse(package_error(response,error), status=status)

def upvote(request):
    return vote(request, 1)

def downvote(request): 
    return vote(request, -1)
