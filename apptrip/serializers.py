from rest_framework import serializers

from .models import PastTravelledTrips, FutureTrips



class Pserializer(serializers.ModelSerializer):
    
    class Meta:
        model = PastTravelledTrips
        fields = ["trip_name","start_date","end_date","days","email","budget","address","location","date_info"]
        # fields = '__all__'
   


class FSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureTrips
        fields = ["trip_name","start_date","end_date","days","email","budget","address","location","date_info"]
        


