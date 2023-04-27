from rest_framework import serializers

from .models import PastTravelledTrips, FutureTrips



class Pserializer(serializers.ModelSerializer):
    
    class Meta:
        model = PastTravelledTrips
        fields = ["Trip_name","Start_date","End_date","Email","Budget","location"]

    # def create(self, validated_data):
    #     locations_data = validated_data.pop('location')
    #     past_trip = PastTravelledTrips.objects.create(**validated_data)
    #     for location_data in locations_data:
    #         Location.objects.create(trip=past_trip, **location_data)
    #     return past_trip
    
    
    # def update(self, instance, validated_data):
    #     locations_data = validated_data.pop('location', [])
    #     instance = super().update(instance, validated_data)
    #     for location_data in locations_data:
    #         location, created = Location.objects.update_or_create(trip=instance, id=location_data.get('id'), defaults=location_data)
    #     return instance


class FSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureTrips
        fields = ['_id','Trip_name','Start_date', 'End_date','Email','Budget']

