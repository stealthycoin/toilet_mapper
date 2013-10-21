from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest
from django.utils.datastructures import MultiValueDictKeyError
class ErrorHandler(object):
    def process_exception(self,request, exception):
        status = "";
        if isinstance(exception, ValueError):
            status = 400
        elif isinstance(exception, KeyError) or isinstance(exception, MultiValueDictKeyError):
            status = 400
        elif isinstance(exception, ObjectDoesNotExist):
            status = 404
        return HttpResponse(str(exception), status = status)
             
        
