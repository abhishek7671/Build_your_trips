from django.shortcuts import render,redirect
from .serializers import Pserializer, FSerializer
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import PastTravelledTrips, FutureTrips
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BasicAuthentication
# from rest_framework.filters import SearchFilter
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.mixins import CreateModelMixin
# from rest_framework.authentication import SessionAuthentication,BasicAuthentication,RemoteUserAuthentication, TokenAuthentication
from rest_framework.decorators import api_view
# from rest_framework import generics
from django.contrib import messages
# from django.http import JsonResponse,HttpResponse
from rest_framework import viewsets
from rest_framework import status
import logging


from rest_framework.views import APIView
from rest_framework.response import Response

# logger = logging.getLogger(__name__)

from bson import ObjectId
import uuid


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .serializers import TripSerializer
# from .models import Trip
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# class TripCreateView(APIView):
#     @swagger_auto_schema(
#         operation_id='Create User',
#         request_body=TripSerializer)
#     def post(self, request, format=None):
#         serializer = TripSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.generics import ListAPIView
# from django_filters.rest_framework import DjangoFilterBackend
# from bson import ObjectId


# class GeneralTrip(ListAPIView):
    
#     queryset = Trip.objects.all()
#     serializer_class = TripSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['trip_name']



# class NaturalTrip(APIView):
#     @swagger_auto_schema(
#         operation_id='NaturalTrip ',
#         request_body=TripSerializer)
#     def get(self, request, _id=None , format=None):
        
#         if _id is not None:
            
#             trip=Trip.objects.get(_id=ObjectId(_id))
#             serializer=TripSerializer(trip)
#             return Response(serializer.data)
#         trip = Trip.objects.all()
#         serializer = TripSerializer(trip, many=True)
#         return Response(serializer.data)



from datetime import timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
# from .models import Trip


class TripView(APIView):
    def post(self, request, trip_id):
        trip = PastTravelledTrips.objects.filter(trip_id=trip_id).first()
        if not trip:
            return Response({'error': 'Trip not found'}, status=404)
        
        output = {}
        for i in range(trip.days):
            date = (trip.start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            places = []
            for j in range(len(trip.location)):
                place = {
                    'name': f'Place {j+1}',
                    'location': trip.location[j],
                    'budget': trip.budget/len(trip.location),
                }
                places.append(place)
            
            output[date] = {
                'Place of Visit': places,
            }
        
        return Response(output)


from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mycol = db['apptrip_pasttravelledtrips']


class Ptrip(APIView):
    def post(self, request, format=None):
        
        serializer = Pserializer(data=request.data)
        trip_id= ObjectId()
        # trip_id = str(trip_id)
        print(trip_id)
        if serializer.is_valid():
            serializer.save()
            
            # mycol.insert_one({
            #     'trip_id':trip_id,
                
            # })
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

class Ftrip(APIView):
    
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
  
    
    
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def ptrip(request):
#     logger.info('ptrip view function')
#     try:
#         if request.method == 'GET':
#             trips = PastTravelledTrips.objects.all()
#             serializer = Pserializer(trips, many=True)
#             return Response(serializer.data)
        
#         elif request.method == 'POST':
            # serializer = Pserializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         elif request.method == 'PUT':
#             trip = PastTravelledTrips.objects.get(pk=request.data.get('id'))
#             serializer = Pserializer(trip, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response (serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         elif request.method == 'DELETE':
#             trip = PastTravelledTrips.objects.get(pk=request.data.get('id'))
#             trip.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
    
#     except PastTravelledTrips.DoesNotExist as e:
#         logger.error(str(e))
#         return Response({'error': 'The trip does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
#     except Exception as e:
#         logger.exception(str(e))
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        






# @api_view(['POST'])
# def ftrip(request):
#     serializer = FSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "successfully added data"})
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Ftrip(APIView):
#     def post(self, request, format=None):
#         serializer = FSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Message added successfully"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# def create(self, request, *args, **kwargs):
#         serializer = FSerializer.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         FSerializer.perform_create(serializer)
#         done=FSerializer.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, done=done)


# class Entry(mixins.ListModelMixin):
#     permission_classes = [IsAuthenticated] 
#     serializer_class = FSerializer
#     queryset = FutureTrips.objects.all()
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


        

# class Ftrip1(UpdateAPIView,DestroyAPIView,RetrieveAPIView):
#     queryset = FutureTrips.objects.all()
#     serializer_class = FSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['Place_name']