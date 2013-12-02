from django.http import *
from django.core.exceptions import ObjectDoesNotExist, FieldError, ValidationError

class InvalidPostError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Middleware():    
     def process_exception(self, request, e):
         if isinstance(e, FieldError) or isinstance(e, AttributeError):
             response = str(e)
             status = 400 
         elif isinstance(e, InvalidPostError):
             status = 415
             response = e.value 
         elif isinstance(e, KeyError):
             status = 400
             response = "Missing " + str(e).replace('\'',"") + " attribute" 
         elif isinstance(e, ValueError) or isinstance(e, ObjectDoesNotExist):
             status = 400
             response = str(e).replace('\'',"")
         elif isinstance(e, ValidationError):
             status = 400
             response = str(e)
         else:
             raise e
         return HttpResponse(response, status=status)
