from django.db import models
import uuid
from djongo import models
# from django.contrib.gis.geos import Point
# from rest_framework_gis.serializers import GeoModelSerializer
# from django.contrib.gis.db import models


class PastTravelledTrips(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Trip_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    days= models.IntegerField()
    Email =  models.EmailField(max_length=70)
    Budget = models.IntegerField()
    address = models.CharField(max_length=45)
    location= models.JSONField(default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    

class PreviousTrips(models.Model):
    ptrip = models.EmbeddedField(model_container=PastTravelledTrips)
    headline = models.CharField(max_length=225)   

    
class FutureTrips(models.Model):
    _id = models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Trip_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    days= models.IntegerField()
    Email =  models.EmailField(max_length=70)
    Budget = models.IntegerField()
    address = models.CharField(max_length=50)
    location= models.JSONField(default=None)
    date_info = models.DateTimeField(auto_now_add=True)
    trip_id = models.CharField(max_length=24)





class Ft(models.Model):
    ftrip = models.EmbeddedField(model_container=FutureTrips)
    build = models.CharField(max_length=200)

    


