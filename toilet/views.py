# Create your views here.
from models import Toilet
from review.models import Review
from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template

def single_toilet_view(req, pk):
    t = Toilet.objects.get(pk=pk)
    reviewed = True if len(Review.objects.filter(toilet=t).filter(user=req.user)) > 0 else False
    
    c = Context({ "t": t, 'has_reviewed' : reviewed })    
    
    return render(req, "single_toilet_view.html", c);
