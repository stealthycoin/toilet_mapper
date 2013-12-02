from django.db import models
from toilet.models import Toilet
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

class Review (models.Model):
    def __unicode__(self):
        return u'%s by %s' % (self.toilet, self.user)

    def setattrs(self,dictionary):
        for k, v in dictionary.items():
            setattr(self,k,v)
            
    toilet = models.ForeignKey(Toilet)
    content = models.TextField(validators=[MinLengthValidator(5)])
    rank = models.SmallIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    up_down_rank = models.SmallIntegerField(null=True)
    user = models.ForeignKey(User, related_name='review_creator')
    date = models.DateTimeField()

class Vote (models.Model):
    def __unicode__(self): return u'%s'%self.user
    review = models.ForeignKey(Review)
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField()

