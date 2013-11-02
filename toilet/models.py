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
    
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    


    #zip = django.contrib.localflavor.USpostalCodeField()

class Flag (models.Model):
    def __unicode__(self): return u'%s'%self.name
    def setattrs(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
    name = models.TextField(unique = True)
    explanation = models.TextField()

# Precomputed flag ranking so we don't have to count votes manually
class FlagRanking (models.Model):
    flag = models.ForeignKey(Flag)
    toilet = models.ForeignKey(Toilet)
    up_down_vote = models.SmallIntegerField(null=True)

class FlagVote (models.Model):
    flag = models.ForeignKey(Flag)
    toilet = models.ForeignKey(Toilet)
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField()
    
admin.site.register(Toilet)
admin.site.register(Flag)
admin.site.register(FlagVote)
admin.site.register(FlagRanking)
        
