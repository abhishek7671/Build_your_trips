from .serializers import Pserializer, FSerializer
from .models import PastTravelledTrips, FutureTrips
from rest_framework import status
from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import uuid

from app.permissions import CustomIsauthenticated

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mycol1 = db['apptrip_pasttravelledtrips']

class Ptrip(APIView):
    def post(self, request, format=None):
        permission_classes = [CustomIsauthenticated]
        user_id=request.user._id
        user_ids=str(user_id)
        trip_id= str(uuid.uuid4())
        serializer = Pserializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            user_obj.trip_id=str(trip_id)
            user_obj.user_id=str(user_ids)
            user_obj.save()
            response_data = {
                "Message": "Post Data Successfully",
                "trip_id": trip_id,
                "user_id": user_ids,
                "Created_Data": serializer.data['date_info']
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class pasttrip(APIView):
    def post(self, request):
        data = request.data
        trip_id = data['trip_id']
        date1 = data['startdate']
        date2 = data['enddate']
        mycol1.update(
            {"trip_id":trip_id},
            {"$set":{"startdate":date1,"enddate":date2}},
            
            )
        
        return Response('success')
    

mycol1 = db['apptrip_pasttravelledtrips']

# class Past(APIView):
#     def get(self, request, pk):
#         collection = mycol1
#         trip = collection.find_one({"trip_id": pk,})
        
#         if trip is None:
#             return Response({"message": "Trip not found"}, status=404)
        
#         trip_id = str(trip["trip_id"])
#         trip_data = {"trip_id": trip_id, "trip_name": trip["trip_name"], "budget": trip["budget"]}
        
#         return Response({"message": "success", "trip": trip_data}, status=200)


class Past(APIView):
    def get(self, request, user_id, trip_id):
        collection = mycol1
        trip = collection.find_one({"user_id": user_id, "trip_id": trip_id})
        
        if trip is None:
            return Response({"message": "Trip not found"}, status=404)
        
        trip_id = str(trip["trip_id"])
        trip_data = {"trip_id": trip_id, "trip_name": trip["trip_name"],"start_date":trip["start_date"],"end_date":trip["end_date"],"days":trip["days"],"email":trip["email"],"budget": trip["budget"],"address":trip["address"],"location":trip["location"],"date_info":trip["date_info"]}
        
        return Response({"message": "success", "trip": trip_data}, status=200)

    
    
    # def get(self, request,pk):
    #     permission_classes = [CustomIsauthenticated]
        
    #     if id is not None:
    #         id = ObjectId(request.user._id)
            

    #         trip=PastTravelledTrips.objects.get(trip_id=pk )
    #         serializer=Pserializer(trip)
    #         return Response(serializer.data)
    #     trip = PastTravelledTrips.objects.all()
    #     serializer = Pserializer(trip, many=True)
    #     return Response(serializer.data)



from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mycol = db['apptrip_futuretrips']

class Create_Travel(APIView):
    def post(self, request, format=None):
        permission_classes = [CustomIsauthenticated]
        user_id=request.user._id
        user_ids=str(user_id)
        trip_id= str(uuid.uuid4())
        serializer = FSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            user_obj.trip_id=str(trip_id)
            user_obj.user_id=str(user_ids)
            user_obj.save()
            response_data = {
                "Message":"Post Data Successfully",
                "trip_id": trip_id,
                "user_id": user_ids,
                "Created_Data":serializer.data['date_info']
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CompleteTrip(APIView):
    def post(self, request):
        data = request.data
        trip_id = data['trip_id']
        date1 = data['startdate']
        date2 = data['enddate']
        mycol.update(
            {"trip_id":trip_id},
            {"$set":{"startdate":date1,"enddate":date2}},
            
            )
        
        return Response('success')



from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView

# class Future(APIView):
#     def get(self, request, pk):
#         collection = mycol
#         trip = collection.find_one({"trip_id": pk,})
        
#         if trip is None:
#             return Response({"message": "Trip not found"}, status=404)
        
#         trip_id = str(trip["trip_id"])
#         trip_data = {"trip_id": trip_id, "trip_name": trip["trip_name"], "budget": trip["budget"]}
        
#         return Response({"message": "success", "trip": trip_data}, status=200)
    
class Future(APIView):
    def get(self, request, user_id, trip_id):
        collection = mycol1
        trip = collection.find_one({"user_id": user_id, "trip_id": trip_id})
        
        if trip is None:
            return Response({"message": "Trip not found"}, status=404)
        
        trip_id = str(trip["trip_id"])
        trip_data = {"trip_id": trip_id, "trip_name": trip["trip_name"],"start_date":trip["start_date"],"end_date":trip["end_date"],"days":trip["days"],"email":trip["email"],"budget": trip["budget"],"address":trip["address"],"location":trip["location"],"date_info":trip["date_info"]}
        
        return Response({"message": "success", "trip": trip_data}, status=200)
    




# class Future(APIView):
#     def get(self,request,pk):
#         collection = mycol
#         trip_id = collection.find_one({"trip_id":pk},{"trip_name":1,"budget":1})
#         print(trip_id)
#         return Response({"message": "success", "trip_id": trip_id}, status=200)
#         # userid=order_id['order_info']

        # collection = db['apptrip_futuretrips']





    # def get(self, request, trip_id=None , format=None):
        
    #     if trip_id is not None:
            
    #         trip=FutureTrips.objects.get(_id=ObjectId(trip_id))
    #         serializer=FSerializer(trip)
    #         return Response(serializer.data)
    #     trip = FutureTrips.objects.all()
    #     serializer = FSerializer(trip, many=True)
    #     return Response(serializer.data)
 


# class TripDetailView(APIView):        
#     def get(self, request, trip_id=None , format=None):
        
#         if trip_id is not None:
            
#             trip=PastTravelledTrips.objects.get(_id=ObjectId(trip_id))
#             serializer=Pserializer(trip)
#             return Response(serializer.data)
#         trip = PastTravelledTrips.objects.all()
#         serializer = Pserializer(trip, many=True)
#         return Response(serializer.data)
    
    
    
    

    # def put(self, request, _id=None, format=None):
    #     if _id is not None:
    #         trip = FutureTrips.objects.get(_id=ObjectId(_id))
    #         serializer = FSerializer(trip, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)
        

    # def patch(self, request, _id=None, format=None):
    #     if _id is not None:
    #         try:
    #             trip = FutureTrips.objects.get(_id=ObjectId(_id))
    #             serializer = FSerializer(trip, data=request.data, partial=True)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 return Response(serializer.data)
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #         except FutureTrips.DoesNotExist:
    #             return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
    #         except Exception as e:
    #             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     else:
    #         return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)



    # def delete(self, request, _id=None, format=None):
    #     if _id is not None:
    #         try:
    #             trip = FutureTrips.objects.get(_id=ObjectId(_id))
    #             trip.delete()
    #             return Response({"message": "Trip deleted successfully."})
    #         except FutureTrips.DoesNotExist:
    #             return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
    #         except Exception as e:
    #             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     else:
    #         return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)
  
    




    

#     def put(self, request, _id=None, format=None):
#         if _id is not None:
#             trip = PastTravelledTrips.objects.get(_id=ObjectId(_id))
#             serializer = Pserializer(trip, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)
        

#     def patch(self, request, _id=None, format=None):
#         if _id is not None:
#             try:
#                 trip = PastTravelledTrips.objects.get(_id=ObjectId(_id))
#                 serializer = Pserializer(trip, data=request.data, partial=True)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data)
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             except PastTravelledTrips.DoesNotExist:
#                 return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)



#     def delete(self, request, _id=None, format=None):
#         if _id is not None:
#             try:
#                 trip = PastTravelledTrips.objects.get(_id=ObjectId(_id))
#                 trip.delete()
#                 return Response({"message": "Trip deleted successfully."})
#             except PastTravelledTrips.DoesNotExist:
#                 return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)




# permission_classes = [CustomIsauthenticated]
#     def post(self, request, format=None):
#         id = ObjectId(request.user._id)
#         serializer = Pserializer(data=request.data)
#         data = request.data
#         if serializer.is_valid():
#             user_obj=serializer.save()
#             user_obj.userID = str(id)
#             user_obj.save()
#             return Response({"message": "Message added successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class Create_Travel(APIView):
#     def post(self, request, format=None):
#         trip_id = ObjectId()
#         trip_id = str(trip_id)
#         serializer = FSerializer(data=request.data)
#         if serializer.is_valid():
#             user_obj = serializer.save()
#             user_obj.trip_id = trip_id

#             if hasattr(request, 'user') and request.user.is_authenticated:
#                 user_obj.user_id = request.user.id
#             else:
#                 user_obj.user_id = None

#             user_obj.save()
#             response_data = {
#                 "Message": "Post Data Successfully",
#                 "trip_id": trip_id,
#                 "user_id": user_obj.user_id,
#                 "Created_Data": serializer.data['date_info']
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)