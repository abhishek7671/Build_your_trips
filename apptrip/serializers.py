from rest_framework import serializers

from .models import PastTravelledTrips, FutureTrips


class Pserializer(serializers.ModelSerializer):
    class Meta:
        model = PastTravelledTrips
        fields = ['id','Place_name','Start_date', 'End_date','Email']



class FSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureTrips
        fields = ['id','Place_name','Start_date', 'End_date','Email']