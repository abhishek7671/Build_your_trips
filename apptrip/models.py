# from django.db import models
# import uuid
from djongo import models
# from django.contrib.gis.geos import Point
# from rest_framework_gis.serializers import GeoModelSerializer
# from django.contrib.gis.db import models


class PastTravelledTrips(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Trip_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    Email = models.EmailField(default = None)
    Budget = models.IntegerField()
    location = models.JSONField()


class PreviousTrips(models.Model):
    ptrip = models.EmbeddedField(model_container=PastTravelledTrips)
    headline = models.CharField(max_length=225)   

# class Location(models.Model):
#     location=models.ForeignKey(PastTravelledTrips, on_delete=models.CASCADE,related_name='user_location', null=True, blank=True)
#     location_name = models.CharField(max_length=200)
#     location_latitude = models.CharField(max_length=200)
#     location_longitude = models.CharField(max_length=200)
    
class FutureTrips(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Trip_name = models.CharField(max_length=100)
    Start_date  =models.DateField(null=True, blank=True) 
    End_date =models.DateField(null=True, blank=True)
    Email =  models.EmailField(max_length=70)
    Budget = models.IntegerField()




class Ft(models.Model):
    ftrip = models.EmbeddedField(model_container=FutureTrips)
    build = models.CharField(max_length=200)

    
