import json
import logging
from django.contrib.auth.models import User, Group
from app.serializers import  UserSerializer
from django.views import View
from django.http import JsonResponse
from rest_framework import status
from django_service import settings
from django.shortcuts import get_object_or_404, get_list_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import User
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse
# from app.encrypt_decrypt import encrypt, decrypt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

logger = logging.getLogger("django_service.service.views")

SECRET_KEY='1234567'
class CreateUser(APIView):

    @swagger_auto_schema(
        operation_id='Create User',
        request_body=UserSerializer)
    def post(self, request, format=None):
        """
                API endpoint that create the user.
        """
        serializer = UserSerializer(data=json.loads(request.body))
        if not serializer.is_valid():
            logger.info("Info: %s",str(serializer.errors))
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.initial_data
        try:
            if User.objects.filter(email=data.get('email')) :
                logger.info("Email and Username Already Exists")
                return JsonResponse({"message": "email already exists"},
                                    status=status.HTTP_400_BAD_REQUEST)
            User.objects.create_user(**data)
            logger.info("User created Successfully")
            return JsonResponse({"message": "user created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Exception while connect to DB %s", e)
            return JsonResponse({"message": "DB connection error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class CustomTokenObtainPairView(TokenObtainPairView): # perfect 
    """
    Override default TokenObtainPairView to use custom token serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer



class ChangePassword(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username or email'),
            'oldpassword': openapi.Schema(type=openapi.TYPE_STRING, description='Type old password'),
            'newpassword': openapi.Schema(type=openapi.TYPE_STRING, description='Type new password')
        }
    ))
    def post(self, request, format=None):
        data = json.loads(request.body)
        try:
            user_obj = User.objects.get(Q(username__iexact=data["username"]) | Q(email__iexact=data["username"]))
            valid = user_obj.check_password(data['oldpassword'])
            if not valid:
                return JsonResponse({"message": "Old Password not match."}, status=status.HTTP_400_BAD_REQUEST)
            user_obj.set_password(data["newpassword"])
            user_obj.save()
            return JsonResponse({"message": "user password updated successfully"})
        except Exception as e:
            logger.exception("Exception while reset the password %s", e)
            return JsonResponse({"message": "Unable to process your request right now."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


# class CustomLogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     @swagger_auto_schema(
#         operation_id='Create User',
#         request_body=UserSerializer)
#     def delete(self, request, *args):
#         tokens = OutstandingToken.objects.filter(user = request.user)
#         for token in tokens:
#             RefreshToken(token).blacklist()
#         return Response({'message':'done'},status=status.HTTP_204_NO_CONTENT)


    



# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
# @swagger_auto_schema(
#     security=[{'Bearer': []}],
#     operation_description='Get a list of all users'
# )
# def user_list(request):
#     """
#     Get a list of all users
#     """
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

# class LogoutAPIView(APIView):
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data.get ["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({'message':'done'},status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        

class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
            return Response({'message':'Done'},status=status.HTTP_205_RESET_CONTENT)
        





# class LogoutAllView(APIView):
# 	"""
# 	It handels the logout from all the devices.
# 	"""

# 	def post(self, request):
# 		tokens = OutstandingToken.objects.filter(user=request.user)

# 		for token in tokens:
# 			BlacklistedToken.objects.get_or_create(token=token)

# 		return Response({"message":"success"},status=status.HTTP_205_RESET_CONTENT)



        

#  modified code
# class Agent_sign_upView(APIView):
#     @swagger_auto_schema(
#         operation_id='Agent_sign_up View',
#         request_body=UserSerializer)
#     def post(self,request,format=None):
#         # import pdb;pdb.set_trace()
#         serializer = UserSerializer(data=json.loads(request.body))
#         data = serializer.initial_data
#         password = data.get("password")
#         password= encrypt(bytes(password, "utf-8"), SECRET_KEY.encode()).decode()
#         data["password"] = password
#         email=data.get("email")
#         existing_user = User.objects.filter(email=email).first()
#         if serializer.is_valid():
#             if existing_user is not None:
#                 return JsonResponse({'Message':'Email alredy exists'})
#             else:
#                 serializer.save()
#                 return JsonResponse({'Message':'User created Sucessfully!'})
#         else:
#             return JsonResponse({'Message':'User not Created!!'})
        


# class AuthenticateUser(APIView):#Working man
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'username': openapi.Schema(type=openapi.TYPE_STRING, description='username '),
#             'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')
#         }
#     ))
#     def post(self, request, format=None):
#         # import pdb;pdb.set_trace()
#         data = json.loads(request.body)
#         user = User.objects.filter(Q(username__iexact=data["username"])).first()
#         if user is not None:
#             encrypted_password = user.password
#             decrypted_password = decrypt(bytes(encrypted_password, "utf-8"), SECRET_KEY.encode()).decode()
#             x= decrypted_password
#             if x == data["password"]:
#                 token, created = Token.objects.get_or_create(user=user)
#                 return JsonResponse({"status": "success", "msg": "user successfully authenticated", "token": token.key})
#             else:
#                 return JsonResponse({"status": "error", "msg": "incorrect password"})
#         else:
#             return JsonResponse({"status": "error", "msg": "incorrect username"})

#___________________________________________________________________________________________________________________________________________
# from pymongo import MongoClient
# import datetime
# from rest_framework.authtoken.models import Token
# client = MongoClient('mongodb://localhost:27017')
# db =client['santhosh']
# mycol = db["token_db"]

# class AuthenticateUser(APIView): # Ganesh Upadted code
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'username': openapi.Schema(type=openapi.TYPE_STRING, description='username '),
#             'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
#         }
#     ))
#     def post(self, request, format=None):
#         #import pdb;pdb.set_trace()        
#         data = json.loads(request.body)
#         # exact=data["password"]
#         # newpass_1= decrypt(bytes(exact, "utf-8"), SECRET_KEY.encode()).decode()
#         # x=newpass_1
#         user = User.objects.filter(Q(username__iexact=data["username"]) | Q(password__iexact=data["password"])).first()
#         if user is not None:
#             username=data.get("username")
#             password_1=data.get("password")
#             newpass_2= decrypt(bytes(password_1, "utf-8"), SECRET_KEY.encode()).decode() 
#             m= newpass_2          
#             if username and m:
#                 newpass_3= decrypt(bytes(password_1, "utf-8"), SECRET_KEY.encode())
#                 y=newpass_3.decode()
#                 if  m == y:
#                     user = authenticate(username=data["username"], password=password_1)
#                     token, created= Token.objects.get_or_create(user=user)
#                     mycol.insert_one({
#                         # "user_id": str(user.id),
#                         "token": token.key,
#                         "created_at": datetime.datetime.now()
#                         })

#                 return JsonResponse({"status": "success", "msg": "user successfully authenticated", "msg1":"log_in the previous page","token": token.key})
#         else:
#             return JsonResponse({"status": "error", "msg": "incorrect username or password"})
# # #__________________________________________________________________________________________________________________________________________________
 
# class ChangePassword(APIView):
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'username': openapi.Schema(type=openapi.TYPE_STRING, description='username or email'),
#             'oldpassword': openapi.Schema(type=openapi.TYPE_STRING, description='Type old password'),
#             'newpassword': openapi.Schema(type=openapi.TYPE_STRING, description='Type new password')
#         }
#     ))
#     def post(self, request, format=None):
#         data = json.loads(request.body)
#         try:
#             user_obj = User.objects.get(Q(username__iexact=data["username"]) | Q(email__iexact=data["username"]))
#             valid = user_obj.check_password(data['oldpassword'])
#             if not valid:
#                 return JsonResponse({"message": "Old Password not match."}, status=status.HTTP_400_BAD_REQUEST)
#             user_obj.set_password(data["newpassword"])
#             user_obj.save()
#             return JsonResponse({"message": "user password updated successfully"})
#         except Exception as e:
#             logger.exception("Exception while reset the password %s", e)
#             return JsonResponse({"message": "Unable to process your request right now."},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class LogoutView(APIView):#Ganesh
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#            properties={
#             'token': openapi.Schema(type=openapi.TYPE_STRING, description='refresh_token')
#         }
#      ))
#     def post(self, request):
#         refresh_token = {'token':"U2FsdGVkX19/FxRrKmASgQw3j83WES5jj5xtOvSgmzc="}
#         if not refresh_token:
#             return Response({"mes": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"mes": str(e)}, status=status.HTTP_400_BAD_REQUEST)

 

# class GetAllUsers(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         """
#         API endpoint that fetch all users.
#         """
#         users_data = User.objects.all().order_by('-date_joined')
#         user_serializer = UserSerializer(users_data, many=True, context={'request': request})
#         return JsonResponse({"users": user_serializer.data})


# class GetUserById(APIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, pk):
#         """
#         API endpoint that fetch user by id.
#         """
#         queryset = User.objects.filter(id=pk)
#         serializer_user = UserSerializer(queryset, many=True, context={'request': request})
#         return JsonResponse({"users": serializer_user.data})


# class ProfileView(APIView):
#     permission_classes = (AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly )

#     def get(self, request, format=None):
#         data = dict()
#         data['username'] = request.user.username
#         data['email'] = request.user.email
#         data['user_id'] = request.user.pk
#         data['token'] = request.auth.token if request.auth else None
#         logger.info("User data %s", data)
#         return Response(data)


# @api_view(['GET'])
# def profile(request):
#     user = request.user  # Get logged-in user object
#     if user.is_authenticated:  # Check if user is authenticated
#         user_data = {
#             'username': user.username,
#             'email': user.email,
#             # 'used_id':user.user_id,
#             # 'token':user.token,

        
#             # Add other user data fields as needed
#         }
#         return Response(user_data)
#     else:
#         return Response({'message': 'User not authenticated'})



# class Agent_signup(APIView):

#     @swagger_auto_schema(
#         operation_id='Create User',
#         request_body=AgentSerializer)
#     def post(self, request, format=None):
#         """
#                 API endpoint that create the user.
#         """
#         serializer = AgentSerializer(data=json.loads(request.body))
#         if not serializer.is_valid():
#             logger.info("Info: %s",str(serializer.errors))
#             return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         data = serializer.initial_data
#         try:
#             if User.objects.filter(email=data.get('email')) :
#                 logger.info("Email and Username Already Exists")
#                 return JsonResponse({"message": "email already exists"},
#                                     status=status.HTTP_400_BAD_REQUEST)
#             User.objects.create_user(**data)
#             logger.info("User created Successfully")
#             return JsonResponse({"message": "user created successfully"}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             logger.exception("Exception while connect to DB %s", e)
#             return JsonResponse({"message": "DB connection error"},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)