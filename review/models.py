from django.db import models
from toilet.models import Toilet
from django.contrib.auth.models import User
from django.contrib import admin

class Review (models.Model):
    toilet = models.ForeignKey(Toilet)
    content = models.TextField()
    rank = models.SmallIntegerField()
    user = models.ForeignKey(User)
    date = models.DateTimeField()

admin.site.register(Review)
    

# Create your models here.
