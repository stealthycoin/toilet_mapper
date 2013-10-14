from toilet.models import Toilet
from django.shortcuts import render
from toilet.views import single_toilet_view as stv
from main.forms import AddRestroomForm


def home(request):
    return render(request, 'home.html')

def single_toilet_view(req, pk):
    return render(req, "toilet.html", { "toilet": stv ( pk ) })

def signin(request):
    return render(request, 'signin.html')

def create(request):
    return render(request, 'create.html')

def add_restroom(request):
    return render(request, 'add_restroom.html', { 'forms' : AddRestroomForm() })


