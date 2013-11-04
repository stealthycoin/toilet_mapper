from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class TimedUser(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField()

admin.site.register(TimedUser)
# Create your models here.
