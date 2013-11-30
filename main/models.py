from django.db import models
from django.contrib.auth.models import User

class AdditionalUserInfo(models.Model):
    user = models.ForeignKey(User)

    male = models.BooleanField()
    female = models.BooleanField()


    def __unicode__(self):
        return u"%s" % self.user
