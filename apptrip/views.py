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
from django.http import Http404
from rest_framework.exceptions import NotFound
import json
from app.permissions import CustomIsauthenticated
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mydb = db['apptrip_pasttravelledtrips']
mycol = db['apptrip_futuretrips']
database = db['spent_amount']
coll = db['average_amount']

from app.authentication import JWTAuthentication

import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('django')
logger = logging.getLogger("django_service.service.views")


class Ptrip(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomIsauthenticated]
    @method_decorator(token_required)
    def post(self, request, format=None):
        try:
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
                logger.info('Success')
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                logger.error("Invalid serializer data")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("An error occurred while processing the request")
            return Response("Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class pasttrip(APIView):
    def post(self, request):
        try:
            data = request.data
            trip_id = data['trip_id']
            trip_details = data['trip_details']
            
            mydb.update(
                {"trip_id": trip_id},
                {"$set": {"trip_details": trip_details}},
            )
            logger.info('Successfully complete')
            return Response('success')
        except KeyError as e:
            logger.error("KeyError occurred: %s", str(e))
            return Response("Missing required data", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("An error occurred while processing the request")
            return Response("Internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    


class Past_User_id(APIView):
    def get(self, request, user_id, format=None):
        try:
            user_objs = PastTravelledTrips.objects.filter(user_id=user_id)
            serializer = Pserializer(user_objs, many=True)
            logger.info('200 ok')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PastTravelledTrips.DoesNotExist:
            logger.critical("User not found.")
            return Response({"Message": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class Past(APIView):
    permission_classes = [CustomIsauthenticated]
    @method_decorator(token_required)
    def get(self, request, user_id, trip_id):
        try:
            db_client = MongoClient('mongodb://localhost:27017')
            db = db_client['santhosh']
            collection = db['apptrip_pasttravelledtrips']

            user = collection.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
            if not user:
                raise Http404

            trip_data = {
                "trip_id": trip_id,
                "trip_name": user["trip_name"],
                "start_date": user["start_date"],
                "end_date": user["end_date"],
                "days": user["days"],
                "email": user["email"],
                "budget": user["budget"],
                "address": user["address"],
                "location": user['location'],
                "date_info": user["date_info"]
            }

            mycol = db['apptrip_pasttravelledtrips']
            user2 = mycol.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})

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
                'trip_details': trip_details
            }
            logger.info('Get the data successfully')
            return Response({"message": "Get the data successfully", "user": trip_data, **response}, status=200)

        except Http404:
            logger.warning("User or trip not found")
            return Response({"message": "User or trip not found"}, status=404)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response({"message": "An error occurred"}, status=500)





class Create_Travel(APIView):
    permission_classes = [CustomIsauthenticated]
    authentication_classes = [JWTAuthentication]
    @method_decorator(token_required)
    def post(self, request, format=None):
        try:
            user_ids = str(request.user._id)
            trip_id = str(uuid.uuid4())
            request.data.update({'user_id': user_ids, 'trip_id': trip_id})
            serializer = FSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "Message": "Post Data Successfully",
                    "trip_id": trip_id,
                    "user_id": user_ids,
                    "Created_Data": serializer.data['date_info']
                }
                logger.info('Success')
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                logger.error("Invalid serializer data")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.critical("Error occurred while creating travel.")
            return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompleteTrip(APIView):
    def post(self, request):
        try:
            data = request.data
            trip_id = data['trip_id']
            data = data['trip_details']
            
            mycol.update(
                {"trip_id": trip_id},
                {"$set": {"trip_details": data}},
            )
            logger.info('Done')
            return Response('success')
        except KeyError:
            logger.warning("Missing required data in CompleteTrip API.")
            return Response("Missing required data.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.critical("Error occurred while completing the trip.")
            return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   


class Future(APIView):
    permission_classes = [CustomIsauthenticated]
    @method_decorator(token_required)
    def get(self, request, user_id, trip_id):
        try:
            db_client = MongoClient('mongodb://localhost:27017')
            db = db_client['santhosh']
            collection = db['apptrip_futuretrips']

            user = collection.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})
            if not user:
                raise NotFound('Trip not found.')

            trip_data = {
                "trip_id": trip_id,
                "trip_name": user["trip_name"],
                "start_date": user["start_date"],
                "end_date": user["end_date"],
                "days": user["days"],
                "email": user["email"],
                "budget": user["budget"],
                "address": user["address"],
                "location": user['location'],
                "date_info": user["date_info"]
            }

            mycol = db['apptrip_futuretrips']
            user2 = mycol.find_one({'user_id': str(user_id), 'trip_id': str(trip_id)})

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
                'trip_details': trip_details
            }
            logger.info('Data retrieved successfully')
            return Response({"message": "Data retrieved successfully", "user": trip_data, **response}, status=200)

        except NotFound as e:
            logger.error('Trip not found')
            return Response({"error": "Trip not found."}, status=404)

        except Exception as e:
            logger.exception('An error occurred')
            return Response({"error": "An error occurred."}, status=500)


class Future_User_id(APIView):
    def get(self, request, user_id, format=None):
        try:
            user_objs = FutureTrips.objects.filter(user_id=user_id)
            serializer = FSerializer(user_objs, many=True)
            data = serializer.data
            logger.info("Data Retrieve user_id")

            return Response(data, status=status.HTTP_200_OK)
        except FutureTrips.DoesNotExist:
            logger.error("User not found for user_id")
            return Response({"Message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("An error occurred for user_id")
            return Response({"Message": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class PostcallAPI(APIView):
    permission_classes = [CustomIsauthenticated]
    @method_decorator(token_required)
    def post(self, request):
        try:
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

            if 'expenses_id' in data and 'expenses_details' in data:
                database.update(
                    {'expense_id': data['expenses_id']},
                    {
                        '$push': {'expenses_details': {'$each': data['expenses_details']}},
                    }
                )
                logger.info('Data successfully updated in the database')
                return Response('success')
            else:
                database.insert_one(request_data)
                logger.info('Data successfully stored in the database')

            return Response(response_data)
        except Exception as e:
            logger.error(f"Error interacting with database")
            return Response({'message': 'Failed to store/update data in the database.'}, status=500)





class ExpensesAPI(APIView):
    def get(self, request, trip_id):
        try:
            expenses = database.find({'trip_id': trip_id})
        except Exception as e:
            logger.critical(f"Error retrieving data")
            return Response({'message': 'Failed to retrieve data from the database.'}, status=500)

        if expenses:
            response_data = []
            for expense in expenses:
                response_data.append({
                    'expense_id': expense['expense_id'],
                    'expenses_details': expense['expenses_details'],
                })
                logger.info('Data Post Successfully')
            return Response(response_data)
        else:
            logger.warning(f"No expenses found for trip_id")
            return Response({'message': 'No expenses found for the given trip_id.'}, status=404)



class GetExpenseAPI(APIView):
    permission_classes = [CustomIsauthenticated]
    @method_decorator(token_required)
    def get(self, request, trip_id, expense_id):
        try:
            result = database.find_one({'trip_id': trip_id, 'expense_id': expense_id})
            if result:
                result['_id'] = str(result['_id'])
                logger.info("Retrieve the Data based on id's ")
                return Response(result)
            else:
                logger.warning("GetExpenseAPI - Expense not found.")
                return Response({'message': 'Expense not found.'}, status=404)
        except Exception as e:
            logger.error("GetExpenseAPI - Error retrieving document.")
            return Response({'message': 'Failed to retrieve data from the database.'}, status=500)



class TotalExpensesAPI(APIView):
    permission_classes = [CustomIsauthenticated]
    @method_decorator(token_required)
    def post(self, request):
        try:
            data = request.data
            trip_id = data.get('trip_id')
            expenses_id = data.get('expenses_id')

            
            logging.debug(f"Received POST request. trip_id: {trip_id}, expenses_id: {expenses_id}")

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
                'trip_id': trip_id,
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

          
            logging.info("Successfully POST ")

            return Response(response_data)

        except Exception as e:
            logging.error("An error occurred")
            return Response({'error': 'An error occurred while processing the request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GetTotalExpensesAPI(APIView):
    permission_classes = [CustomIsauthenticated]
    @method_decorator(token_required)
    def get(self, request, trip_id):
        expense_data = coll.find_one({'trip_id': trip_id})

        if not expense_data:
            logger.error("Total expenses data not found for trip ID")
            return Response({'error': 'Total expenses data not found.'}, status=404)
        expense_data['_id'] = str(expense_data['_id'])
        logger.info("Total expenses data retrieved successfully for trip ID")
        return Response(expense_data)



