from django.db import models
from django.contrib.auth.models import AbstractUser
from djongo import models

class USER_details(models.Model):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    NORMAL_USER = 'Normal User'
    USER_TYPES = [
        (NORMAL_USER, 'Normal User'),
    ]
    usertype = models.CharField(max_length=20,choices=USER_TYPES,default=NORMAL_USER,editable=False)
    username = models.CharField(max_length=138)
    email = models.EmailField()
    password = models.CharField(max_length=138)
    date_joined = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    username=models.CharField(max_length=50,)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    password=models.CharField(default=None, max_length=180)
    # mobile = models.CharField(default=None, max_length=15, blank=True, null=True)

