from django.shortcuts import render,redirect
from .serializers import Pserializer, FSerializer
from rest_framework.generics import UpdateAPIView, ListAPIView,CreateAPIView,RetrieveAPIView, DestroyAPIView
from .models import PastTravelledTrips, FutureTrips
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
# from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view
# from rest_framework import generics
from django.contrib import messages
# from django.http import JsonResponse,HttpResponse
from rest_framework import viewsets
from rest_framework import status
import logging


from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# this code is on class based views 

class Ptrip(viewsets.ModelViewSet):
    queryset = PastTravelledTrips.objects.all()
    serializer_class = Pserializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Place_name']



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ptrip(request):
    logger.info('ptrip view function')
    try:
        if request.method == 'GET':
            trips = PastTravelledTrips.objects.all()
            serializer = Pserializer(trips, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = Pserializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'PUT':
            trip = PastTravelledTrips.objects.get(pk=request.data.get('id'))
            serializer = Pserializer(trip, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response (serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            trip = PastTravelledTrips.objects.get(pk=request.data.get('id'))
            trip.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    except PastTravelledTrips.DoesNotExist as e:
        logger.error(str(e))
        return Response({'error': 'The trip does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        logger.exception(str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        





class Ptrip1(RetrieveAPIView):
    queryset = PastTravelledTrips.objects.all()
    serializer_class = Pserializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Place_name']

@api_view(['POST'])
def ftrip(request):
    serializer = FSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "successfully added data"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ftrip(APIView):
    def post(self, request, format=None):
        serializer = FSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message added successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Ftrip1(viewsets.ModelViewSet):
    queryset = FutureTrips.objects.all()
    serializer_class = FSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['Place_name']


def create(self, request, *args, **kwargs):
        serializer = FSerializer.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        FSerializer.perform_create(serializer)
        done=FSerializer.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, done=done)


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