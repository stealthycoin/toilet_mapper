from models import Toilet, Flag, FlagVote, FlagRanking
from review.models import Review
import json
from common.middletier import post_to_dict, serialize, currentTime, package_error
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required


#just using for debugging
import sys


#this adds a toilet using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = request.POST.copy()
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


#upvote downvote system
@transaction.commit_on_success
def flag_vote(request, new_vote):
    error = ''
    response = ''
    """ Save this for later. 
        error = 'You are clever but not that clever my little pet.'
        + ' BTW our team is super excited about our river boat tour '
        + ' Check out http://vikingrivercruises.com. Some crazy amazing boat touring going on there. '
        + ' I mean really I never even thought about river cruises. Cruises on a river? Sign me up. '
    """
    status = 201
    if not request.user.is_authenticated():
      error += "Must be logged in"
      status = 403
    elif request.method == 'POST':
        data = request.POST
        t = Toilet.objects.get(pk=data['toilet_pk'])
        f = Flag.objects.get(pk=data['flag_pk'])
        try:
            r = FlagRanking.objects.get(toilet = t, flag = f)
        except FlagRanking.DoesNotExist:
            r = FlagRanking(flag = f, toilet = t, up_down_vote = 0)
        try:
            prev_vote_obj = FlagVote.objects.get(flag=f, toilet = t, user = request.user)
            prev_vote = prev_vote_obj.vote
            if new_vote != prev_vote:
                prev_vote_obj.delete()
                r.up_down_vote += new_vote
        except FlagVote.DoesNotExist:
            r.up_down_vote += new_vote
            v = FlagVote(user = request.user, flag = f, toilet = t, vote = new_vote)
            v.save()
        r.save()
        response = serialize([r])
    else:
        error += 'No POST data in request.\n'
        status = 415
    return HttpResponse(package_error(response,error), status=status)

def flag_upvote(request): return flag_vote(request, 1)

def flag_downvote(request): return flag_vote(request, -1)
