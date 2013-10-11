from django.shortcuts import render
from toilet.views import single_toilet_view as stv

def home(request):
    return render(request, 'home.html')

def single_toilet_view(req, pk):
    return render(req, "toilet.html", { "toilet": stv(pk)} )

