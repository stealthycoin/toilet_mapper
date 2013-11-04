from django.db import models
from toilet.models import Toilet
from django.contrib.auth.models import User

class Review (models.Model):
    def __unicode__(self): return u'%s'%self.user

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
    def __unicode__(self): return u'%s'%self.user
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField()

