from django.http import *
from django.core.exceptions import ObjectDoesNotExist, FieldError
from common.models import TimedUser
from common.middletier import currentTime

class InvalidPostError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Middleware():    
    def process_request(self, request):
        if request.path == '/api/user/create/' and request.user.is_authenticated():
            return HttpResponse("Can't create an account you are logged in", status=415)

        if request.path == '/api/user/create/' and request.method == 'POST' and request.user.is_authenticated():
            user = request.user
            try:
                userTime = TimedUser.objects.get(user=user)
            except ObjectDoesNotExist:
                userTime = TimedUser()
                userTime.user = user
                userTime.time = currentTime() 
                userTime.save()
            print (currentTime() - userTime.time).total_seconds()
            if (currentTime() - userTime.time).total_seconds() < 0.02:
                return HttpResponse("To many posts persecond", status=403)
            userTime.time = currentTime()
            userTime.save()

        return None

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
        if isinstance(e, ObjectDoesNotExist) or isinstance(e, DoesNotExist):
            status = 404
            response = str(e).replace('\'',"")

        return HttpResponse(response, status=status)
