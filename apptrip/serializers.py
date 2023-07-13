from rest_framework import serializers
from .models import FutureTrips



   


class FSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureTrips
        fields = ["trip_name","start_date","end_date","days","email","budget","address","location","date_info","trip_id","user_id"]



































# class MyModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Budget
#         fields = ['date', 'name', 'description', 'amount']






        


