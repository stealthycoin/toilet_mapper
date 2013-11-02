from django.http import *
from django.core.exceptions import ObjectDoesNotExist

class InvalidPostError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Middleware():    
    def process_exception(self, request, e):
        print "AM I ALIVE??"
        response = "dunno man"
        status = 500
        if isinstance(exception, InvalidPostError):
            status = 415
            response = e.value 
        if isinstance(exception, KeyError):
            status = 400
            response = "Missing " + str(e).replace('\'',"") + " attribute" 
        if isinstance(exception, ValueError):
            status = 400
            response = str(e).replace('\'',"")
        if isinstance(exception, ObjectDoesNotExist):
            status = 404
            response = str(e).replace('\'',"")

        return HttpResponse(response, status=status)
