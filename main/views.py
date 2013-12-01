from toilet.models import Toilet
from django.shortcuts import render
from django.template import Context, RequestContext
from toilet.views import single_toilet_view as stv
from main.forms import AddRestroomForm
from django.contrib.auth.models import User
from models import AdditionalUserInfo

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
    

