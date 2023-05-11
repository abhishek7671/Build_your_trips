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
        enddate = user2['enddate']
        startdate = user2['startdate']
       
        # Get start date locations tr

        
        startdate_locations = []
        for date,place_info in startdate.items():
            for visit in place_info['Place of Visit']:
        #         startdate_locations.append({
        #             'date':visit['date'],
        #             'name': visit['name'],
        #             'budget':visit['budget'],
        #             'location': visit['location']
                    
        #         })
                placename= visit['name']
                li_1=visit['location'][0]
                lo_1=visit['location'][1]
                google_maps_url_1 = f'https://www.google.com/maps/dir/?api=1&origin={li_1},{lo_1}'
                response_1 = {
            
            'name': visit['name'],
            'budget':visit['budget'], 
            'location': google_maps_url_1
        }
        # Get end date locations
        enddate_locations = []
        for date, place_info in enddate.items():
            for visit in place_info['Place of Visit']:
                
                
                place= visit['name']
                li=visit['location'][0]
                lo=visit['location'][1]
                google_maps_url_2 = f'https://www.google.com/maps/dir/?api=1&origin={li},{lo}'
                response_2 = {
            'name': visit['name'],
            'budget':visit['budget'],
            "location": google_maps_url_2,
        }
        response = {
            'main_location': google_maps_url,
            'startdate_locations': response_1,
            'enddate_locations': response_2
        }

        return Response({
            "message": "get the data successfully",
            "user": trip_data,
            **response
        }, status=200)



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


    

from rest_framework.views import APIView
from rest_framework.response import Response
from pymongo import MongoClient
from django.http import Http404

class Futurelocation(APIView):
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
        enddate = user2['enddate']
        startdate = user2['startdate']
       
        # Get start date locations

        
        startdate_locations = []
        for date,place_info in startdate.items():
            for visit in place_info['Place of Visit']:
        #         startdate_locations.append({
        #             'date':visit['date'],
        #             'name': visit['name'],
        #             'budget':visit['budget'],
        #             'location': visit['location']
                    
        #         })
                placename= visit['name']
                li_1=visit['location'][0]
                lo_1=visit['location'][1]
                google_maps_url_1 = f'https://www.google.com/maps/dir/?api=1&origin={li_1},{lo_1}'
                response_1 = {
            
            'name': visit['name'],
            'budget':visit['budget'], 
            'location': google_maps_url_1
        }
        # Get end date locations
        enddate_locations = []
        for date, place_info in enddate.items():
            for visit in place_info['Place of Visit']:
                
                
                place= visit['name']
                li=visit['location'][0]
                lo=visit['location'][1]
                google_maps_url_2 = f'https://www.google.com/maps/dir/?api=1&origin={li},{lo}'
                response_2 = {
            'name': visit['name'],
            'budget':visit['budget'],
            "location": google_maps_url_2,
        }
        response = {
            'main_location': google_maps_url,
            'startdate_locations': response_1,
            'enddate_locations': response_2
        }

        return Response({
            "message": "get the data successfully",
            "user": trip_data,
            **response
        }, status=200)


# class Geolocation (APIView):
#     permission_classes=[CustomIsauthenticated]
#     def get(self, request):
#         user_id=ObjectId(request.user._id)
#         print(user_id)
#         collection = db['apptrip_futuretrips']
#         user = collection.find_one({'user_id':str(user_id)})
#         location=user['location']
#         x=location[0]
#         y=location[1]
#         response=({'location': 'https://www.google.com/maps/dir/?api=1' + '&origin=' + f'{x},{y}'})
#         return Response(response)




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
        trip_data = {"trip_id": trip_id, 
                     "trip_name": user["trip_name"],
                     "start_date":user["start_date"],
                     "end_date":user["end_date"],
                     "days":user["days"],
                     "email":user["email"],
                     "budget": user["budget"],
                     "address":user["address"],
                     "date_info":user["date_info"]}
        
        mycol = db['apptrip_futuretrips']
        user2 = mycol.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
        enddate = user2['enddate']
        startdate = user2['startdate']
       
        # Get start date locations

        
        startdate_locations = []
        for date,place_info in startdate.items():
            for visit in place_info['Place of Visit']:
                startdate_locations.append({
                    
                    'name': visit['name'],
                    'budget':visit['budget'],
                    'location': visit['location']
                    
                })

        # Get end date locations
        enddate_locations = []
        for date, place_info in enddate.items():
            for visit in place_info['Place of Visit']:
                enddate_locations.append({
                    
                    'name': visit['name'],
                    'budget':visit['budget'],
                    'location': visit['location']
                    
                })
                response = {
            'main_location': google_maps_url,
            'startdate_locations': startdate_locations,
            'enddate_locations': enddate_locations
        }

        
        return Response({"message": "get the data successfully", "user": trip_data, **response},status=200)


