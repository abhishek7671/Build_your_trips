from .serializers import Pserializer, FSerializer,Aserializer
from .models import PastTravelledTrips, FutureTrips
from rest_framework.decorators import api_view
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


@api_view(['POST'])
def AverageAmountView_post(request):
    serializer = Aserializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    budget_details = serializer.validated_data['budget_details']
    
    response_data = []

    for detail in budget_details:
        # day = detail.get('day',None)
        day_budget = detail.get('day_budget', None)
        date = detail.get('date', None)
        names = detail.get('name', [])
        amounts = detail.get('amount', [])
        total_amount = sum(amounts)
        average = total_amount / len(names)

        data = {
            # 'day':day,
            'day_budget': day_budget,
            'date': date,
            'average': average,
        }

        for i, name in enumerate(names):
            contribution = amounts[i]
            difference = contribution - average

            data[f'{name}_contributed'] = contribution
            data[f'{name}_difference'] = difference

        response_data.append(data)

    response = {
        'message': 'data posted successfully',
        'data': response_data,
    }

    return Response(response)





# tfyufgcghuytfgcuyiuhcuyfgcvhuoiuhhuyoihuyghvbvuyhbiyfgxcvkuyrdrsxvbbjhytrdfgxcbv btrdxcvfftyh


# from rest_framework.views import APIView
# from rest_framework.response import Response
# import uuid
# from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017')
# data = client['santhosh']
# database = data['apptrip_mymodel']

# class ExpenseAPIView(APIView):
#     def post(self, request):
#         expenses = request.data.get('expenses_details', [])
#         result = []
#         unique_dates = set()

#         for expense in expenses:
#             date = expense['date']
#             if date in unique_dates:
#                 continue
#             unique_dates.add(date)

#             total_amount = sum(expense['amount'] for expense in expenses if expense['date'] == date)
#             count = len([expense for expense in expenses if expense['date'] == date])
#             average = total_amount / count if count > 0 else 0

#             contributions = {}
#             differences = {}
#             individuals = set(expense['name'] for expense in expenses)
#             for individual in individuals:
#                 contributions[individual] = sum(expense['amount'] for expense in expenses if expense['date'] == date and expense['name'] == individual)
#                 differences[individual] = contributions[individual] - average

#             expense_data = {
#                 'date': date,
#                 'total_amount': str(total_amount),
#                 'average': float(average),
#                 **{f'{name}_contributed': contributions.get(name, 0) for name in individuals},
#                 **{f'{name}_difference': differences.get(name, -average) for name in individuals},
#             }
#             result.append(expense_data)

#             expense_id = str(uuid.uuid4())

#         response_data = {
#             'message': 'Data posted successfully',
#             'expenses_details': result,
#             'expenses_id': str(expense_id),  # Convert expense_id to string
#         }

#         try:
            
#             database.insert_one(response_data.copy())
#         except Exception as e:
#             print(f"Error inserting document: {e}")

#         return Response(response_data)


# class ExpenseView(APIView):
#     def get(self, request, expenses_id):
#         try:
           
#             document = database.find_one({'expenses_id': expenses_id})
#             if document:
#                 document.pop('_id')
#                 return Response(document)
#             else:
#                 return Response({'message': 'Expense not found'}, status=404)
#         except Exception as e:
#             return Response({'message': f'Error retrieving expense: {e}'}, status=500)


# awsedrfguirdfghiutrsgdfkuiluuyetrtyuiotrydfsguyirtdfguytersfgxchjliutuydgfckyyrtdfchkjyutgdtrtdfrtf56rtfgr67ftg5rtfgrtfcvrtfgcvytfgcvtyfg




from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
data = client['santhosh']
database = data['apptrip_mymodel']

class ExpenseAPIView(APIView):
    def post(self, request):
        expenses = request.data.get('expenses_details', [])
        result = []
        unique_dates = set()

        for expense in expenses:
            date = expense['date']
            if date in unique_dates:
                continue
            unique_dates.add(date)

            total_amount = sum(expense['amount'] for expense in expenses if expense['date'] == date)
            count = len([expense for expense in expenses if expense['date'] == date])
            average = total_amount / count if count > 0 else 0

            contributions = {}
            differences = {}
            individuals = set(expense['name'] for expense in expenses)
            for individual in individuals:
                contributions[individual] = sum(expense['amount'] for expense in expenses if expense['date'] == date and expense['name'] == individual)
                differences[individual] = contributions[individual] - average

            expense_data = {
                'date': date,
                'total_amount': str(total_amount),
                'average': float(average),
                **{f'{name}_contributed': contributions.get(name, 0) for name in individuals},
                **{f'{name}_difference': differences.get(name, -average) for name in individuals},
            }
            result.append(expense_data)

        total_expenses = {
            'total_budget': str(sum(expense['amount'] for expense in expenses)),
            'total_average': float(sum(expense['amount'] for expense in expenses) / len(expenses)) if len(expenses) > 0 else 0,
            **{f'total_{name}_contributed': sum(expense['amount'] for expense in expenses if expense['name'] == name) for name in individuals},
            **{f'total_{name}_difference': sum(expense['amount'] for expense in expenses if expense['name'] == name) - (sum(expense['amount'] for expense in expenses) / len(expenses)) if len(expenses) > 0 else 0 for name in individuals},
        }

        expense_id = str(uuid.uuid4())

        response_data = {
            'message': 'Data posted successfully',
            'expenses_details': result,
            'expenses_id': expense_id,
            'total_expenses_details': [total_expenses],
        }

        try:
            database.insert_one(response_data.copy())
        except Exception as e:
            print(f"Error inserting document: {e}")

        return Response(response_data)







class DifferenceAPIView(APIView):
    def get(self, request, trip_id):
      
        expense_data = database.find_one({'trip_id': trip_id})

        if expense_data:
           
            expense_data['_id'] = str(expense_data['_id'])
            return Response(expense_data)
        else:
            return Response({'message': 'Expense data not found'}, status=404)



class DifferenceAPI(APIView):
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





    





# from bson import ObjectId
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017')
# data = client['santhosh']
# database = data['apptrip_mymodel']

# class ExpenseView(APIView):
#     def get(self, request, expenses_id):
    
#         try :
#             expense_data = database.find_one({'expenses_id': expenses_id})
#             if expense_data:
                
#                 expense_data.pop('_id')
#                 return Response(expense_data)
#             else:
#                 return Response({'message': 'Expense data not found'}, status=404)
#         except Exception as e:
#             print(f"Error retrieving document: {e}")
#             return Response({'message': 'Internal server error'}, status=500)






# from rest_framework.views import APIView
# from rest_framework.response import Response
# from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017')
# data = client['santhosh']
# database = data['apptrip_mymodel']

# class ExpenseDetailAPIView(APIView):
#     def get(self, request, trip_id, expenses_id):  # Corrected argument name to 'expenses_id'
#         try:
#             # Find the document based on trip_id and expenses_id
#             document = database.find_one({'trip_id': trip_id, 'expenses_id': expenses_id})

#             if document:
#                 # Extract the relevant data
#                 expenses_details = document.get('expenses_details', [])
#                 total_expenses_details = document.get('total_expenses_details', [])

#                 response_data = {
#                     'message': 'Data retrieved successfully',
#                     'expenses_details': expenses_details,
#                     'total_expenses_details': total_expenses_details,
#                 }
#                 return Response(response_data)
#             else:
#                 response_data = {'message': 'Data not found'}
#                 return Response(response_data, status=404)

#         except Exception as e:
#             print(f"Error retrieving document: {e}")
#             response_data = {'message': 'An error occurred while retrieving data'}
#             return Response(response_data, status=500)







from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
data = client['santhosh']
database = data['spent_amount']

class PostcallAPI(APIView):
    def post(self, request):
        trip_id = request.data.get('trip_id')
        expenses = request.data.get('expenses_details', [])

        expense_id = str(uuid.uuid4())
        request_data = {
            'trip_id': trip_id,
            'expense_id': expense_id,
            'expenses_details': expenses,
        }
        response_data = {
            'message': 'Data posted successfully',
            'expenses_id': expense_id,
        }

        try:
            database.insert_one(request_data)
        except Exception as e:
            print(f"Error inserting document: {e}")
            return Response({'message': 'Failed to store data in the database.'}, status=500)

        return Response(response_data)


class complete_expense(APIView):
    def post(self, request):
        data = request.data
        expenses_id = data['expenses_id']
        expenses_details = data['expenses_details']

        try:
            database.update(
                {'expense_id': expenses_id},
                {
                    '$push': {'expenses_details': {'$each': expenses_details}},
                }
            )
        except Exception as e:
            print(f"Error updating document: {e}")
            return Response({'message': 'Failed to update data in the database.'}, status=500)

        return Response('success')



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





































        


























































