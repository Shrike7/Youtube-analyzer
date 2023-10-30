from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)


class Chanel(models.Model):
    custom_id = models.CharField(primary_key=True, max_length=30, unique=True,)
    name = models.CharField(max_length=256)


class UserProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Video(models.Model):
    custom_id = models.CharField(primary_key=True, max_length=11, unique=True)
    name = models.CharField(max_length=256)
    chanel = models.ForeignKey(Chanel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class WatchRecord(models.Model):
    time = models.DateTimeField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_profile', 'video', 'time')
