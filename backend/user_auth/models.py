from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profilePictureUrl = models.URLField(blank=True, null=True)
    profileUsername = models.CharField(max_length=30)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Video(models.Model):

    videoId = models.CharField(max_length=255, unique=True)
    channelId = models.CharField(max_length=255)
    channelTitle = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.URLField()
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
