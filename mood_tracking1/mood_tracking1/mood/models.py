from django.db import models
from django.contrib.auth.models import User, Permission


class Activity_event(models.Model):
    type = models.IntegerField()
    event = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()


class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)

class Friend(models.Model):
    user_id = models.IntegerField()
    added_time = models.DateTimeField(auto_now_add=True)
    friend_id = models.IntegerField()


class ConsultingSession(models.Model):
    Client_name = models.CharField()
    Client_location = models.CharField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    phone_number = models.CharField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class MoodComparison(models.Model):
    your_mood = models.IntegerField()
    your_user_id = models.IntegerField()
    compared_mood = models.IntegerField()
    compared_user_id = models.IntegerField()
    description = models.CharField()
    title = models.CharField()