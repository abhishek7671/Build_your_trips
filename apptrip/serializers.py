from rest_framework import serializers
from .models import FutureTrips



# class Pserializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = PastTravelledTrips
#         fields = ["trip_name","start_date","end_date","days","email","budget","address","location","date_info","trip_id","user_id"]
#         # fields = '__all__'
   


class FSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureTrips
        fields = ["trip_name","start_date","end_date","days","email","budget","address","location","date_info","trip_id","user_id"]





# class Aserializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contributor  # Add the model attribute
#         fields = ["budget_details"]



# class Eserializer(serializers.ModelSerializer):
#     trip_id = serializers.CharField()
#     class Meta:
#         model =Expense
#         # fields = ["date","time","name","description","amount","place_of_expense"]
#         fields = "__all__"
        






























# class MyModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Budget
#         fields = ['date', 'name', 'description', 'amount']






        


