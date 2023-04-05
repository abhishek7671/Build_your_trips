from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username=models.CharField(max_length=50,)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    password=models.CharField(default=None, max_length=180)
    # mobile = models.CharField(default=None, max_length=15, blank=True, null=True)
