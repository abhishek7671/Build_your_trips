# from django.db import models
# import uuid
from djongo import models

class PastTravelledTrips(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Place_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    Email = models.EmailField(default = None)

class PreviousTrips(models.Model):
    ptrip = models.EmbeddedField(model_container=PastTravelledTrips)
    headline = models.CharField(max_length=225)

    
class FutureTrips(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Place_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    Email =  models.EmailField(max_length=70)



class Ft(models.Model):
    ftrip = models.EmbeddedField(model_container=FutureTrips)
    build = models.CharField(max_length=200)

    
