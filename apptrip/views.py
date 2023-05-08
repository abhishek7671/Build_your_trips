from .serializers import Pserializer, FSerializer
from .models import PastTravelledTrips, FutureTrips
from rest_framework import status
from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Ptrip(APIView):
    def post(self, request, format=None):
        
        serializer = Pserializer(data=request.data)
        trip_id= ObjectId()
        print(trip_id)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post data successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Past(APIView):
    def get(self, request, _id=None , format=None):
        
        if _id is not None:
            
            trip=PastTravelledTrips.objects.get(_id=ObjectId(_id))
            serializer=Pserializer(trip)
            return Response(serializer.data)
        trip = PastTravelledTrips.objects.all()
        serializer = Pserializer(trip, many=True)
        return Response(serializer.data)
    

    def put(self, request, _id=None, format=None):
        if _id is not None:
            trip = PastTravelledTrips.objects.get(_id=ObjectId(_id))
            serializer = Pserializer(trip, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request, _id=None, format=None):
        if _id is not None:
            try:
                trip = PastTravelledTrips.objects.get(_id=ObjectId(_id))
                serializer = Pserializer(trip, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except PastTravelledTrips.DoesNotExist:
                return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, _id=None, format=None):
        if _id is not None:
            try:
                trip = PastTravelledTrips.objects.get(_id=ObjectId(_id))
                trip.delete()
                return Response({"message": "Trip deleted successfully."})
            except PastTravelledTrips.DoesNotExist:
                return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)

    
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mycol = db['apptrip_futuretrips']

class Create_Travel(APIView):
    
    def post(self, request, format=None):
        id = ObjectId()
        id = str(id)
        serializer = FSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.save()
            user_obj.trip_id=id
            user_obj.save()
            response_data = {
                "Message":"Post Data Successfully",
                "trip_id":id,
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
            {"$set":{"startdate":date1,"enddate":date2}}
            )
        
        return Response('success')



class Future(APIView):
    def get(self, request, _id=None , format=None):
        
        if _id is not None:
            
            trip=FutureTrips.objects.get(_id=ObjectId(_id))
            serializer=FSerializer(trip)
            return Response(serializer.data)
        trip = FutureTrips.objects.all()
        serializer = FSerializer(trip, many=True)
        return Response(serializer.data)
    

    def put(self, request, _id=None, format=None):
        if _id is not None:
            trip = FutureTrips.objects.get(_id=ObjectId(_id))
            serializer = FSerializer(trip, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request, _id=None, format=None):
        if _id is not None:
            try:
                trip = FutureTrips.objects.get(_id=ObjectId(_id))
                serializer = FSerializer(trip, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except FutureTrips.DoesNotExist:
                return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, _id=None, format=None):
        if _id is not None:
            try:
                trip = FutureTrips.objects.get(_id=ObjectId(_id))
                trip.delete()
                return Response({"message": "Trip deleted successfully."})
            except FutureTrips.DoesNotExist:
                return Response({"error": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "No _id provided"}, status=status.HTTP_400_BAD_REQUEST)
  
    
