from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Toilet (models.Model):
    def __unicode__(self): return u'%s'%self.name

    def setattrs(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    def updateRating(self, newRating):
        numerator = (float(self.rating) * float(self.numberOfReviews)) + float(newRating)
        self.numberOfReviews = self.numberOfReviews + 1
        self.rating = numerator/self.numberOfReviews 
        self.save()

    date = models.DateTimeField()
    creator = models.ForeignKey(User)
    name = models.CharField(max_length = 128)
    numberOfReviews = models.IntegerField(default=0)
    rating = models.DecimalField(default=5.0, max_digits=11, decimal_places=10) 
    lat = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=10, decimal_places=6, null=True)
   
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
        
