from django.db import models
import uuid

class PastTravelledTrips(models.Model):
    id = models.IntegerField(primary_key=True)
    Place_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    Email = models.EmailField(default = None)


    
class FutureTrips(models.Model):
    id = models.IntegerField(primary_key=True)
    Place_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    Email =  models.EmailField(max_length=70)
    
