from django.db import models
from toilet.models import Toilet
from django.contrib.auth.models import User
from django.contrib import admin

class Review (models.Model): 
    def setattrs(self,dictionary):
        for k, v in dictionary.items():
            setattr(self,k,v)

    toilet = models.ForeignKey(Toilet)
    content = models.TextField()
    rank = models.SmallIntegerField()
    up_down_rank = models.SmallIntegerField(null=True)
    user = models.ForeignKey(User, related_name='review_creator')
    date = models.DateTimeField()

class Vote (models.Model):
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField()

admin.site.register(Review)
admin.site.register(Vote)
    

# Create your models here.
