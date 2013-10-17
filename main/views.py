from toilet.models import Toilet
from django.shortcuts import render
from django.template import Context
from toilet.views import single_toilet_view as stv
from main.forms import AddRestroomForm


def home(request):
    return render(request, 'home.html')

def signin(request):
    print request.GET;
    c = Context({ "GET": request.GET });
    return render(request, 'signin.html', c)

def create_user(request):
    return render(request, 'create_user.html')

def add_restroom(request):
    return render(request, 'add_restroom.html', { 'forms' : AddRestroomForm() })

def signed_up(request):
    return render(request, 'signed-up.html')

def gmap(request):
    return render(request, 'gmap.html')

