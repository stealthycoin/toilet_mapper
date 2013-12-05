from toilet.models import Toilet
from django.shortcuts import render
from django.template import Context, RequestContext
from toilet.views import single_toilet_view as stv
from main.forms import AddRestroomForm
from django.contrib.auth.models import User
from models import AdditionalUserInfo
from common.middletier import distance, squareBounds

def home(request):
    return render(request, 'home.html')

def signin(request):
    print request.GET;
    c = Context({ "GET": request.GET });
    return render(request, 'signin.html', c)

def faq(request):
    return render(request, 'faq.html')

def create_user(request):
    return render(request, 'create_user.html')

def add_restroom(request):
    return render(request, 'add_restroom.html', { 'forms' : AddRestroomForm() })

def signed_up(request):
    return render(request, 'signed-up.html')

def gmap(request):
    return render(request, 'gmap.html')

def profile(request, user):
    print User.objects.get(username__exact=user)
    p = User.objects.get(username__exact=user)
    try:
        info = AdditionalUserInfo.objects.get(user=p)
    except AdditionalUserInfo.DoesNotExist:
        info = AdditionalUserInfo(user=p,male=False,female=False)
        info.save()
    c = RequestContext(request, {"p": p, "info": info, "can_edit": p == request.user})
    return render(request, 'profile.html', c)
    


def emergency(req):
    A = B
    current_lat = float(req.COOKIES.get('lat'))
    current_lng = float(req.COOKIES.get('lng'))

    sq0 = squareBounds(current_lat, current_lng, 10)
    sq = sq0.copy()
    sq["x_left"] = min( sq0["x_left"], sq0["x_right"])
    sq["x_right"] = max( sq0["x_left"], sq0["x_right"])
    sq["y_bottom"] = min( sq0["y_bottom"], sq0["y_top"])
    sq["y_top"] = max( sq0["y_bottom"], sq0["y_top"])
    filters = {"lat__gt": sq["x_left"],"lat__lt": sq["x_right"], "lng__gt":sq["y_bottom"], "lng__lt":sq["y_top"]}
    qs = Toilet.objects.all().filter(**filters)
    if len(qs) == 0: 
        return render(req, 'emergency_notfound.html')

    # These comparisson functions use eachother to break ties
    #  which is why they pass an optional `final` argument.
    def distanceCmp(t1, t2, final=False):
        d1 = distance(current_lat, current_lng, t1.lat, t1.lng)
        d2 = distance(current_lat, current_lng, t2.lat, t2.lng)
        if d1 == d2: 
            if(final == True): return 0
            else: return ratingCmp(t1, t2, True);
        return -1 if d1 < d2 else 1
    def ratingCmp(t1, t2, final=False):
        if t1.rating == t2.rating: 
            if(final == True): return 0
            else: return distanceCmp(t1, t2, True);
        return -1 if t1.rating > t2.rating else 1

    qs = list(qs)
    qs.sort(cmp=distanceCmp)
    return stv(req, qs[0].pk);
