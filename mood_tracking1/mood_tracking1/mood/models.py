from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Activity_event(models.Model):
    type = models.IntegerField()
    event = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)


