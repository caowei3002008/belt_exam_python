from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

from django.db import models


class User(AbstractUser, models.Model):
    name = models.CharField(max_length=250)
    alias = models.CharField(max_length=250)
    username = models.CharField(max_length=250, default="None", editable=False, unique=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Friends(models.Model):
    user_friend = models.ForeignKey(User, related_name='requester')
    second_friend = models.ForeignKey(User, related_name='accepter')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)