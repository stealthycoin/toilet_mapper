# Create your views here.
from models import Toilet
from django.template import Template, Context
from django.template.loader import get_template

def single_toilet_view(pk):
    t = Toilet.objects.get(pk=pk)
    c = Context({ "t": t })
    return get_template("single_toilet_view.html").render(c)
