from rest_framework import serializers

from .models import PastTravelledTrips, FutureTrips



class Pserializer(serializers.ModelSerializer):
    
    class Meta:
        model = PastTravelledTrips
        fields = ["Trip_name","Start_date","End_date","Email","Budget","location"]

   


class FSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureTrips
        fields = ['_id','Trip_name','Start_date', 'End_date','Email','Budget','location','date_info']
        


