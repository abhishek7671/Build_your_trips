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



logger = logging.getLogger('django')
# logger = logging.getLogger("django_service.service.views")

from django.core.mail import EmailMessage



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

            # Send email to all email addresses
            email_addresses = request.data.get('email', [])
            subject = "Hi all"  # Specify the subject of the email
            message = "Shall we go for a trip?"  # Specify the body of the email

            for email_address in email_addresses:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email='BUILDYOURTRIP<abhisheksuda123@gmail.com>',
                    to=[email_address],
                )
                email.send()

            response_data = {
                "Message": "Post Data Successfully",
                "trip_id": trip_id,
                "user_id": user_ids,
                "Created_Data": serializer.data['date_info']
            }
            logger.info('Success')
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.critical("Error occurred while creating travel.")
            return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            logger.info('Done')
            return Response('success')

        except Exception as e:
            logger.critical("Error occurred while completing the trip: %s", e)
            return Response("An error occurred.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   

class Future(APIView):
    permission_classes = [CustomIsauthenticated]

    @method_decorator(token_required)
    def get(self, request, user_id, trip_id):
        try:
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

            logger.info('Data retrieved successfully')
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
            logger.info("Data Retrieve user_id")

            return Response(data, status=status.HTTP_200_OK)
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
                logger.info('Data successfully updated in the database')
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
            expense_data = database.find_one({'expense_id': expenses_id})
            expenses_details = expense_data['expenses_details']

            missing_fields = [field for field in ['trip_id', 'expenses_id'] if not data.get(field)]
            if missing_fields:
                return Response({'error': f"Missing required field(s): {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total budget and contributions
            total_budget = sum(float(expense['amount']) for expense in expenses_details)
            total_contributions = {
                f'total_{email}_contributed': sum(float(expense['amount']) for expense in expenses_details if expense['email'] == email)
                for email in expense_data['trip_emails']
            }

            # Calculate differences
            total_differences = {
                f'total_{email}_difference': total_contributions[f'total_{email}_contributed'] - (total_budget / len(expense_data['trip_emails']))
                for email in expense_data['trip_emails']
            }

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

            response_data_json = json.loads(json.dumps(response_data, default=str))
            coll.insert_one(response_data_json)

            for email in expense_data['trip_emails']:
                mail_content = f'''
                <h2>Expense Details for Trip ID: {trip_id}</h2>
                <p>Total Budget: {total_budget}</p>
                <p>Total Average: {total_average}</p>
                <p>Total Contributions by {email}: {total_contributions[f'total_{email}_contributed']}</p>
                <p>Total Difference for {email}: {total_differences[f'total_{email}_difference']}</p>
                '''

                message = MIMEMultipart()
                message['From'] = 'BUILDYOURTRIP<abhisheksuda123@gmail.com>'
                message['To'] = email
                message['Subject'] = 'Expense Details'

                message.attach(MIMEText(mail_content, 'html'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login('abhisheksuda123@gmail.com', 'eduq yzha uota wayx')
                    server.send_message(message)

            logger.info("Successfully POST")

            return Response(response_data)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





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



