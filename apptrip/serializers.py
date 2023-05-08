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
        fields = ['_id','Trip_name','Start_date', 'End_date','Email','Budget','location','date_info']
        # fields = "__all__"


# from rest_framework import serializers
# from .models import Trip

# class TripSerializer(serializers.ModelSerializer):
#     total_places = serializers.SerializerMethodField()

#     class Meta:
#         model = Trip
#         fields = '__all__'
#         read_only_fields = ['total_places']

#     def get_total_places(self, obj):
#         return len(obj.visiting_places)

#     def create(self, validated_data):
#         # Exclude the computed total_places field from the validated data
#         total_places = validated_data.pop('total_places', None)

#         # Create the Trip object
#         trip = Trip.objects.create(**validated_data)

#         # Set the computed total_places value on the Trip object
#         trip.total_places = total_places

#         return trip