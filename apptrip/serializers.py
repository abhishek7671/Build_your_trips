from rest_framework import serializers

from .models import PastTravelledTrips, FutureTrips


class Pserializer(serializers.ModelSerializer):
    class Meta:
        model = PastTravelledTrips
        fields = ['_id','Place_name','Start_date', 'End_date','Email']



class FSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureTrips
        fields = ['_id','Place_name','Start_date', 'End_date','Email']