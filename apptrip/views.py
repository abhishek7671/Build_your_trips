from .serializers import Pserializer, FSerializer
from .models import PastTravelledTrips, FutureTrips
from rest_framework import status
from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import Http404
import uuid

from app.permissions import CustomIsauthenticated

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mydb = db['apptrip_pasttravelledtrips']


class Ptrip(APIView):
    permission_classes = [CustomIsauthenticated]
    def post(self, request, format=None):
        user_ids=str(request.user._id)
        trip_id= str(uuid.uuid4())
        request.data.update({'user_id':user_ids,'trip_id':trip_id})
        serializer = Pserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
            data = data['trip_details']
            
            mydb.update(
                {"trip_id":trip_id},
                {"$set":{"trip_details":data}},
                
                )
            
            return Response('success')
    


class Past_User_id(APIView):
    def get(self, request, user_id, format=None):
        try:
            user_objs = PastTravelledTrips.objects.filter(user_id=user_id)
            serializer = Pserializer(user_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PastTravelledTrips.DoesNotExist:
            return Response({"Message": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class Past(APIView):
    permission_classes = [CustomIsauthenticated]

    def get(self, request, user_id, trip_id):
        db_client = MongoClient('mongodb://localhost:27017')
        db = db_client['santhosh']
        collection = db['apptrip_pasttravelledtrips']

        user = collection.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
        if not user:
            raise Http404

        location = user['location']
        x = location[0]
        y = location[1]

        google_maps_url = f'https://www.google.com/maps/dir/?api=1&origin={x},{y}'
        trip_data = {
            "trip_id": trip_id,
            "trip_name": user["trip_name"],
            "start_date": user["start_date"],
            "end_date": user["end_date"],
            "days": user["days"],
            "email": user["email"],
            "budget": user["budget"],
            "address": user["address"],
            "date_info": user["date_info"]
            
        }
        mycol = db['apptrip_pasttravelledtrips']
        user2 = mycol.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
        trip_details = user2['trip_details']
        # Generate trip details
        trip_details = []
        if "trip_details" in user2:
            for detail in user2["trip_details"]:
                trip_details.append({
                    "day": detail["day"],
                    "date": detail["date"],
                    "visit_place": detail["visit_place"],
                    "budget": detail["budget"],
                    "location": detail["location"]
                })

        response = {
            'main_location': google_maps_url,
            'trip_details': trip_details
        }

        return Response({"message": "get the data successfully", "user": trip_data, **response}, status=200)
    



from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mycol = db['apptrip_futuretrips']

class Create_Travel(APIView):
    permission_classes = [CustomIsauthenticated]
    def post(self, request, format=None):
        user_ids=str(request.user._id)
        trip_id= str(uuid.uuid4())
        request.data.update({'user_id':user_ids,'trip_id':trip_id})
        serializer = FSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
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
            data = data['trip_details']
            
            mycol.update(
                {"trip_id":trip_id},
                {"$set":{"trip_details":data}},
                
                )
            
            return Response('success')
    



from django.http import Http404

class Future(APIView):
    permission_classes = [CustomIsauthenticated]

    def get(self, request, user_id, trip_id):
        db_client = MongoClient('mongodb://localhost:27017')
        db = db_client['santhosh']
        collection = db['apptrip_futuretrips']

        user = collection.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
        if not user:
            raise Http404

        location = user['location']
        x = location[0]
        y = location[1]

        google_maps_url = f'https://www.google.com/maps/dir/?api=1&origin={x},{y}'
        trip_data = {
            "trip_id": trip_id,
            "trip_name": user["trip_name"],
            "start_date": user["start_date"],
            "end_date": user["end_date"],
            "days": user["days"],
            "email": user["email"],
            "budget": user["budget"],
            "address": user["address"],
            "date_info": user["date_info"]
            
        }
        mycol = db['apptrip_futuretrips']
        user2 = mycol.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
        trip_details = user2['trip_details']
        # Generate trip details
        trip_details = []
        if "trip_details" in user2:
            for detail in user2["trip_details"]:
                trip_details.append({
                    "day": detail["day"],
                    "date": detail["date"],
                    "visit_place": detail["visit_place"],
                    "budget": detail["budget"],
                    "location": detail["location"]
                })

        response = {
            'main_location': google_maps_url,
            'trip_details': trip_details
        }

        return Response({"message": "get the data successfully", "user": trip_data, **response}, status=200)


class Future_User_id(APIView):
    def get(self, request, user_id, format=None):
        try:
            user_objs = FutureTrips.objects.filter(user_id=user_id)
            serializer = FSerializer(user_objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FutureTrips.DoesNotExist:
            return Response({"Message": "User not found."}, status=status.HTTP_404_NOT_FOUND)






