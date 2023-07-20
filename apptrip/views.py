import logging
import json
from .serializers import FSerializer
from .models import FutureTrips
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from django.utils.decorators import method_decorator
from app.utils import token_required
from rest_framework.exceptions import NotFound
from app.authentication import JWTAuthentication
from app.permissions import CustomIsauthenticated
from django.core.mail import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mydb = db['apptrip_pasttravelledtrips']
mycol = db['apptrip_futuretrips']
collection = db['apptrip_futuretrips']
database = db['spent_amount']
coll = db['average_amount']


logger = logging.getLogger('custom_logger')
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from email.utils import formataddr

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

            if not serializer.is_valid():
                logger.error("Invalid serializer data")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()


            email_addresses = request.data.get('email', [])
            trip_data = {
                'address': request.data.get('address', ''),
                'start_date': request.data.get('start_date', ''),
                'end_date': request.data.get('end_date', ''),
                'trip_name': request.data.get('trip_name', ''),
                'email': request.data.get('email', []),
            }
            self.send_emails(email_addresses, trip_data)

            response_data = {
                "Message": "Post Data Successfully",
                "trip_id": trip_id,
                "user_id": user_ids,
                "Created_Data": serializer.data['date_info']
            }
            logger.info('Post Data Successfully')
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.critical("Error occurred while creating travel.")
            return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_emails(self, email_addresses, trip_data):
        subject = 'Successfully Created A Trip'
        sender_name = 'Build Your Trips'
        sender_email = 'abhisheksuda123@example.com'
        template_name = 'index.html'

        for email in email_addresses:
            try:
                
                html_message = render_to_string(template_name, trip_data)
                plain_message = strip_tags(html_message)
                formatted_sender = formataddr((sender_name, sender_email))

                send_mail(subject, plain_message, formatted_sender, [email], html_message=html_message)
            except ValidationError:
                logger.error(f"Invalid email address: {email}")
            except Exception as e:
                logger.error(f"Error sending email to {email}: {str(e)}")






class CompleteTrip(APIView):
    def post(self, request):
        try:
            data = request.data
            trip_id = data.get('trip_id')
            trip_details = data.get('trip_details')

            missing_fields = [field for field in ['trip_id', 'trip_details'] if not data.get(field)]

            if missing_fields:
                return Response({'error': f"Missing required field(s): {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)
            mycol.update(
                {"trip_id": trip_id},
                {"$set": {"trip_details": trip_details}},
            )
            logger.info('Completely Fill The Trip Details')
            return Response('success')

        except Exception as e:
            logger.critical("Error occurred while completing the trip: %s", e)
            return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   

class Future(APIView):
    permission_classes = [CustomIsauthenticated]

    @method_decorator(token_required)
    def get(self, request, trip_id):
        try:
            user = collection.find_one({'trip_id': str(trip_id)})
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
            user2 = mycol.find_one({'trip_id': str(trip_id)})

            trip_details = [{
                "day": detail["day"],
                "date": detail["date"],
                "visit_place": detail["visit_place"],
                "budget": detail["budget"],
                "location": detail["location"]
            } for detail in user2["trip_details"]] if "trip_details" in user2 else []

            response = {
                'trip_details': trip_details
            }

            logger.info('Data Retrieved Successfully Based on Trip_id')
            return Response({"message": "Data retrieved successfully", "user": trip_data, **response}, status=200)

        except Exception as e:
            logger.exception('An error occurred')
            return Response({"error": "An error occurred."}, status=500)


class Future_User_id(APIView):
    def get(self, request, user_id, format=None):
        try:
            user_objs = FutureTrips.objects.filter(user_id=user_id)
            serializer = FSerializer(user_objs, many=True)
            data = serializer.data
            logger.info("Data Retrieved Based on User_id")

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("An error occurred for user_id")
            return Response({"Message": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetTripDetails(APIView):
    def get(self, request, email):
        try:
            trips = FutureTrips.objects.filter(email__icontains=email)
            trip_details = []
            for trip in trips:
                trip_details.append({
                    "trip_id": str(trip.trip_id),
                    "trip_name": trip.trip_name,
                    "days": trip.days,
                    "start_date": trip.start_date.strftime("%Y-%m-%d"),
                    "end_date": trip.end_date.strftime("%Y-%m-%d"),
                    "email": trip.email,
                    "budget": str(trip.budget),
                    "address": trip.address,
                    "location": trip.location,
                    "user_id": str(trip.user_id),
                })
            response_data = {
                "email": email,
                "trips": trip_details,
                "count": len(trip_details)
            }
            logger.info("Data Retrieved Successfully Based on Email")
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)





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
            missing_fields = [field for field, condition in [('trip_id', not trip_id), ('trip_emails', not trip_emails or not isinstance(trip_emails, list)), ('expenses_details', not expenses or not isinstance(expenses, list))] if condition]

            if missing_fields:
                return Response({'error': f"Missing or invalid required field(s): {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

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
                logger.info('Data Successfully Updated in the Database')
                return Response('success')
            else:
                database.insert_one(request_data)
                logger.info('Data successfully stored in the database')

            return Response(response_data)
        except Exception as e:
            logger.error(f"Error interacting with the database")
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
                logger.info("Retrieve the Data Based on Trip_id and Expense_id ")
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
            expense_data = database.find_one({'expense_id': expenses_id})
            expenses_details = expense_data['expenses_details']

            missing_fields = [field for field in ['trip_id', 'expenses_id'] if not data.get(field)]
            if missing_fields:
                return Response({'error': f"Missing required field(s): {', '.join(missing_fields)}"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Calculate total budget and contributions
            total_budget = sum(float(expense['amount']) for expense in expenses_details)
            total_contributions = {
                f'total_{email}_contributed': round(sum(float(expense['amount']) for expense in expenses_details if
                                                   expense['email'] == email))
                for email in expense_data['trip_emails']
            }

            # Calculate differences
            total_differences = {
                f'total_{email}_difference': round(total_contributions[f'total_{email}_contributed'] - (
                            total_budget / len(expense_data['trip_emails'])))
                for email in expense_data['trip_emails']
            }

            # Calculate total average
            total_average = round(total_budget / len(expense_data['trip_emails']))

            response_data = {
                'trip_id': trip_id,
                'expenses_id': str(expenses_id),
                'total_expenses_details': [
                    {
                        'total_budget': total_budget,
                        'total_average': total_average,
                        **total_contributions,
                        **total_differences
                    }
                ]
            }

            response_data_json = json.loads(json.dumps(response_data, default=str))
            coll.insert_one(response_data_json)

            self.send_email(expense_data['trip_emails'], total_budget, total_average, total_contributions,
                            total_differences)

            logger.info("Successfully POST")

            return Response(response_data)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_email(self, email_addresses, total_budget, total_average, total_contributions, total_differences):
        subject = 'Trip Budget Spents'
        sender_name = 'Build Your Trips'
        sender_email = 'abhisheksuda123@example.com'
        template_name = 'details.html'

        for email in email_addresses:
            try:
                email_data = {
                    'total_budget': total_budget,
                    'total_average': total_average,
                    'total_contributions': total_contributions,
                    'total_differences': total_differences
                }
                html_message = render_to_string(template_name, email_data)
                plain_message = strip_tags(html_message)
                formatted_sender = formataddr((sender_name, sender_email))

                send_mail(subject, plain_message, formatted_sender, [email], html_message=html_message)
            except ValidationError:
                logger.error(f"Invalid email address: {email}")
            except Exception as e:
                logger.error(f"Error sending email to {email}: {str(e)}")




class LastExpenseDetailsAPI(APIView):
    def get(self, request, trip_id):
        try:
          
            expense_data = coll.find_one({'trip_id': trip_id}, sort=[('_id', -1)])
            if not expense_data:
                return Response({'error': 'Expense details not found for the given trip_id'}, status=status.HTTP_404_NOT_FOUND)

            total_expenses_details = expense_data['total_expenses_details']
            last_expense_details = total_expenses_details[-1]
            logger.info('Retrieve the Latest Data Successfully')
            return Response(last_expense_details)

        except Exception as e:
            logger.error('Invalid data')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




