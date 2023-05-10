from django.db import models

from djongo import models



class PastTravelledTrips(models.Model):
    _id = models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.CharField(max_length=50)
    trip_name = models.CharField(max_length=100)
    start_date  =models.DateField(null=True, blank=True) 
    end_date =models.DateField(null=True, blank=True)
    days= models.CharField(max_length=140)
    email =  models.JSONField(default=None)
    budget = models.IntegerField()
    address = models.CharField(max_length=45)
    location= models.JSONField(default=None)
    date_info = models.DateTimeField(auto_now_add=True)
    trip_id = models.CharField(max_length=24)
    
    



class FutureTrips(models.Model):
    _id = models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.CharField(max_length=50)
    trip_name = models.CharField(max_length=100)
    start_date  =models.DateField(null=True, blank=True) 
    end_date =models.DateField(null=True, blank=True)
    days= models.IntegerField()
    email =  models.JSONField(default=None)
    budget = models.IntegerField()
    address = models.CharField(max_length=50)
    location= models.JSONField(default=None)
    date_info = models.DateTimeField(auto_now_add=True)
    trip_id = models.CharField(max_length=24)

    

    


