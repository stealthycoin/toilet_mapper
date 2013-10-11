from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Toilet (models.Model):
    def __unicode__(self): return u'%s'%self.name

    def setattrs(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    date = models.DateTimeField()
    creator = models.ForeignKey(User)
    name = models.CharField(max_length = 64)
    #zip = django.contrib.localflavor.USpostalCodeField()
    
admin.site.register(Toilet)
        
