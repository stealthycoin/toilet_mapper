from models import Toilet
import json

#this adds a toilet using the post data
def add(request):
    error = ''
    response = ''
    status = 201

    
    if request.method == 'POST':
        data = request.POST
        print data

    else:
        error += 'No POST data in request\n'

