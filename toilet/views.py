# Create your views here.
from models import Toilet
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template

def single_toilet_view(req, pk):
    t = Toilet.objects.get(pk=pk)
    c = Context({ "t": t })
    return render(req, "single_toilet_view.html", c);
