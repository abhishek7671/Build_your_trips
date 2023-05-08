from django.db import models
from djongo import models

class USER_details(models.Model):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    email = models.EmailField()
    password = models.CharField(max_length=138)
    date_joined = models.DateTimeField(auto_now_add=True)
    

