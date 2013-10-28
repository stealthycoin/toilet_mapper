from models import Toilet, Flag, FlagVote, FlagRanking
from review.models import Review
import json
from common.middletier import post_to_dict, serialize, currentTime, package_error
from django.http import HttpResponse

#just using for debugging
import sys


#this adds a toilet using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    if request.method == 'POST':
        data = request.POST.copy()
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
    nameFilter = False
    
    post_dict = request.POST
    
    if 'creator' in post_dict:
      nameFilter = True
    

    toilet_set = Toilet.objects.all()
    review_set = Review.objects.all()

    l = []
    
    #I'm using this to filter toilets by user. Probably a better way.
    if nameFilter == True:
      toilet_set = toilet_set.filter(creator=post_dict['creator'])
    for t in toilet_set:
        t_rs = review_set.filter(toilet=t)
        total = 0.0
        count = len(list(t_rs))
        if count == 0:
            total = -1
        else:
            for r in t_rs:
                total += r.rank
            total /= count
        
        l.append({"t" : json.loads(serialize([t])), "ranking" : total, "count" : count})
        
    response = json.dumps(l)
    return HttpResponse(response,status=status)

def flag_retrieve_rankings(request):
    response = ''
    error = ''
    status = 201
    if request.method == 'POST':
        data = request.POST
        t = Toilet.objects.get(pk=data['toilet_pk'])        
        try:
            r = FlagRanking.objects.get(toilet = t.pk)
            response = serialize([r])
        except FlagRanking.DoesNotExist:
            response = serialize([])

    return HttpResponse(package_error(response,error), status=status)

def flag_retrieve_flags(request):
    response = ''
    error = ''
    status = 201
    f = Flag.objects.get()
    try:
        response = serialize([Flag.objects.get()])
    except ObjectDoesNotExist:
        response = serialize([])
    return HttpResponse(package_error(response,error), status=status)


#upvote downvote system
def flag_vote(request, new_vote):
    error = ''
    """ Save this for later. 
        error = 'You are clever but not that clever my little pet.'
        + ' BTW our team is super excited about our river boat tour '
        + ' Check out http://vikingrivercruises.com. Some crazy amazing boat touring going on there. '
        + ' I mean really I never even thought about river cruises. Cruises on a river? Sign me up. '
    """
    status = 201
    if request.method == 'POST':
        data = request.POST
        f = Flag.objects.get(pk=data['flag_pk'])
        t = Toilet.objects.get(pk=data['toilet_pk'])
        try:
            r = FlagRanking.objects.get(flag = f.pk, toilet = t.pk)
        except FlagRanking.DoesNotExist:
            r = FlagRanking(flag = f, toilet = t, up_down_vote = 0)
        try:
            prev_vote_obj = FlagVote.objects.get(flag=f, toilet = t, user = request.user)
            prev_vote = prev_vote_obj.vote
            if new_vote != prev_vote:
                prev_vote_obj.delete()
                r.up_down_rank += new_vote
        except ObjectDoesNotExist:
            r.up_down_rank += new_vote
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
