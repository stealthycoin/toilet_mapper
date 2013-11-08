from django.http import *
from django.core.exceptions import ObjectDoesNotExist, FieldError

class InvalidPostError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Middleware():    
    def process_exception(self, request, e):
        response = str(e)
        status = 500
        if isinstance(e, FieldError) or isinstance(e, AttributeError):
            response = str(e)
            status = 400 
        if isinstance(e, InvalidPostError):
            status = 415
            response = e.value 
        if isinstance(e, KeyError):
            status = 400
            response = "Missing " + str(e).replace('\'',"") + " attribute" 
        if isinstance(e, ValueError):
            status = 400
            response = str(e).replace('\'',"")
        if isinstance(e, ObjectDoesNotExist):
            status = 404
            response = str(e).replace('\'',"")

        return HttpResponse(response, status=status)
