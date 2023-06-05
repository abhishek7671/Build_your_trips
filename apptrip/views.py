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
from django.utils.decorators import method_decorator
from app.utils import token_required

from app.permissions import CustomIsauthenticated
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mydb = db['apptrip_pasttravelledtrips']


from app.authentication import JWTAuthentication

class Ptrip(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomIsauthenticated]
    def post(self, request, format=None):
        user_ids = str(request.user._id)
        trip_id = str(uuid.uuid4())
        request.data.update({'user_id': user_ids, 'trip_id': trip_id})
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
    authentication_classes = [JWTAuthentication]
    def get(self, request, user_id, trip_id):
        db_client = MongoClient('mongodb://localhost:27017')
        db = db_client['santhosh']
        collection = db['apptrip_pasttravelledtrips']

        user = collection.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
        if not user:
            raise Http404

        
        # x = location[0]
        # y = location[1]

        # google_maps_url = f'https://www.google.com/maps/dir/?api=1&origin={x},{y}'
        trip_data = {
            "trip_id": trip_id,
            "trip_name": user["trip_name"],
            "start_date": user["start_date"],
            "end_date": user["end_date"],
            "days": user["days"],
            "email": user["email"],
            "budget": user["budget"],
            "address": user["address"],
            "location" : user['location'],
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
            # 'main_location': google_maps_url,
            'trip_details': trip_details
        }

        return Response({"message": "get the data successfully", "user": trip_data, **response}, status=200)



from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mycol = db['apptrip_futuretrips']

class Create_Travel(APIView):
    permission_classes = [CustomIsauthenticated]
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
    def get(self, request, user_id, trip_id):
        db_client = MongoClient('mongodb://localhost:27017')
        db = db_client['santhosh']
        collection = db['apptrip_futuretrips']

        user = collection.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
        if not user:
            raise Http404

    
        # x = location[0]
        # y = location[1]

        # google_maps_url = f'https://www.google.com/maps/dir/?api=1&origin={x},{y}'
        trip_data = {
            "trip_id": trip_id,
            "trip_name": user["trip_name"],
            "start_date": user["start_date"],
            "end_date": user["end_date"],
            "days": user["days"],
            "email": user["email"],
            "budget": user["budget"],
            "address": user["address"],
            "location" : user['location'],
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
            # 'main_location': google_maps_url,
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




from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
data = client['santhosh']
database = data['spent_amount']

class PostcallAPI(APIView):
    def post(self, request):
        data = request.data
        trip_id = data.get('trip_id')
        trip_emails = data.get('trip_emails', [])
        expenses = data.get('expenses_details', [])
        expense_id = str(uuid.uuid4())

        request_data = {
            'trip_id': trip_id,
            'trip_emails': trip_emails,
            'expense_id': expense_id,
            'expenses_details': expenses,
        }
        response_data = {
            'message': 'Data posted successfully',
            'expenses_id': expense_id,
        }

        try:
            if 'expenses_id' in data and 'expenses_details' in data:
                database.update(
                    {'expense_id': data['expenses_id']},
                    {
                        '$push': {'expenses_details': {'$each': data['expenses_details']}},
                    }
                )
                return Response('success')
            else:
                database.insert_one(request_data)
        except Exception as e:
            print(f"Error interacting with database: {e}")
            return Response({'message': 'Failed to store/update data in the database.'}, status=500)

        return Response(response_data)







class ExpensesAPI(APIView):
    def get(self, request, trip_id):
        try:
            expenses = database.find({'trip_id': trip_id})
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return Response({'message': 'Failed to retrieve data from the database.'}, status=500)

        if expenses:
            response_data = []
            for expense in expenses:
                response_data.append({
                    'expense_id': expense['expense_id'],
                    'expenses_details': expense['expenses_details'],
                })
            return Response(response_data)
        else:
            return Response({'message': 'No expenses found for the given trip_id.'}, status=404)




class GetExpenseAPI(APIView):
    def get(self, request, trip_id, expense_id):
        try:
            result = database.find_one({'trip_id': trip_id, 'expense_id': expense_id})
            if result:
                
                result['_id'] = str(result['_id'])
                return Response(result)
            else:
                return Response({'message': 'Expense not found.'}, status=404)
        except Exception as e:
            print(f"Error retrieving document: {e}")
            return Response({'message': 'Failed to retrieve data from the database.'}, status=500)





from pymongo import MongoClient
from bson import ObjectId
from rest_framework.response import Response
from rest_framework.views import APIView
import json

client = MongoClient('mongodb://localhost:27017')
data = client['santhosh']
coll = data['average_amount']


class TotalExpensesAPI(APIView):
    def post(self, request):
        data = request.data
        trip_id = data.get('trip_id')
        expenses_id = data.get('expenses_id')

        expense_data = database.find_one({'expense_id': expenses_id})
        expenses_details = expense_data['expenses_details']

        # Calculate total budget and contributions
        total_budget = sum(float(expense['amount']) for expense in expenses_details)
        total_contributions = {}
        for email in expense_data['trip_emails']:
            total_contributions[f'total_{email}_contributed'] = sum(
                float(expense['amount']) for expense in expenses_details if expense['email'] == email
            )

        # Calculate differences
        total_differences = {}
        for email in expense_data['trip_emails']:
            total_differences[f'total_{email}_difference'] = total_contributions[f'total_{email}_contributed'] - (
                        total_budget / len(expense_data['trip_emails']))

        # Calculate total average
        total_average = total_budget / len(expense_data['trip_emails'])

        response_data = {
            'trip_id':trip_id,
            'expenses_id': str(expenses_id),  # Convert ObjectId to string
            'total_expenses_details': [
                {
                    'total_budget': total_budget,
                    'total_average': total_average,
                    **total_contributions,
                    **total_differences
                }
            ]
        }
        
        response_data_json = json.loads(json.dumps(response_data, default=str))  # Convert ObjectId to string in JSON
        
        coll.insert_one(response_data_json)  # Insert the response data into MongoDB

        return Response(response_data)



class GetTotalExpensesAPI(APIView):
    def get(self, request, trip_id):
        expense_data = coll.find_one({'trip_id': trip_id})

        if not expense_data:
            return Response({'error': 'Total expenses data not found.'}, status=404)
        expense_data['_id'] = str(expense_data['_id'])

        return Response(expense_data)



