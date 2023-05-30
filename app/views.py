from django.conf import settings
import jwt
from datetime import timedelta,datetime
import json
import logging
from app.serializers import  USER_Serializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.hashers import make_password, check_password
from .models import USER_details
from .backend import EmailBackend
from rest_framework.generics import CreateAPIView
from app.permissions import CustomIsauthenticated
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from pymongo import MongoClient
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient['santhosh']
mycol3 = mydb['app_user_details']
mytokens=mydb['tokens']

logger = logging.getLogger("django_service.service.views")

JWT_SECRET_KEY = 'django-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02'
JWT_ACCESS_TOKEN_EXPIRATION = 60
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'

def get_token_for_user(user):
    token_payload = {
                'user_id': str(user._id),
                'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION),
                'iat': datetime.utcnow()
                }
    access_token = jwt.encode(token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)

    refresh_token_payload = {
                'user_id': str(user._id),
                'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_TOKEN_EXPIRATION),
                'iat': datetime.utcnow()
                }
    refresh_token = jwt.encode(refresh_token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    return {
        'access':access_token,
        'refresh':refresh_token

    }
class Register(APIView):
    def post(self, request, format=None):
        serializer = USER_Serializer(data=json.loads(request.body))
        if serializer.is_valid():
            data = serializer.validated_data
            password = data['password']
            hased_password = make_password(password)
            email = data['email']
            existing_user = USER_details.objects.filter(email=email).first()
            if existing_user is not None:
                return JsonResponse({'Message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(password=hased_password)
                return JsonResponse({'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'Message': 'User not created'}, status=status.HTTP_400_BAD_REQUEST)
  
class LoginView(APIView):
    def post(self,request):
        data = request.data
        email = data.get('email',None)
        password = data.get('password',None)
        user=EmailBackend.authenticate(self, request, username=email, password=password)
        if user is not None:
            token=get_token_for_user(user)

            return JsonResponse({
                    "status": "success",
                    "msg": "user successfully authenticated",
                    "token": token,
                    "user_id": str(user._id),
                })
        else:
            return JsonResponse({"message":"invalid data"})


class ChangePassword(CreateAPIView):

    def post(self,request):

        data = request.data
        email = data['email']
        oldpassword = data['password']
        newpassword = data['newpassword']
        try:
            user_obj = USER_details.objects.get(email=email)
        except USER_details.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not check_password(oldpassword, user_obj.password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        user_obj.password=make_password(newpassword)
        user_obj.save()
        return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
    

import secrets 
def generate_otp(length=6):
        """Generates a random OTP of the specified length."""
        return secrets.token_hex(length // 2 + 1)[:length]



class ForgotPassword(APIView):
    def post(self,request):
        data= request.data
        email=data["email"]
        try:
            user_obj = USER_details.objects.get(email=email)
        except USER_details.DoesNotExist:
            return Response({'error': 'Email doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)
        if user_obj is not None:
            otp = generate_otp()
            hased_password = make_password(otp)
            mycol3.update(
                    {"email": email},
                    {
                        "$set": {"password":hased_password}
                    }
                )
            email_msg = EmailMessage(
            'Email Details',
            f"RESET PASSWORD \n Hey there!\n It looks like you are trying to reset password.\n\nYOUR NEW LOGIN DETAILS:\n password: {otp}\n Email: {email}",
            settings.EMAIL_HOST_USER,
            [email],
            )
            email_msg.send(fail_silently=True)
            return Response({"message":"New password generated successfully and send to your respective mail id"})
        else:
            return JsonResponse({"message":"invalid data"})


class LogoutView(APIView): # logout function for normal user.
    permission_classes = [CustomIsauthenticated]
    def post(self,request):
        user_id = request.user._id
        auth_header = request.headers.get('Authorization')
        a_token = auth_header.split()[1]
        user_data = mytokens.find({})    
        information=[]
        for info in user_data:
            if ((datetime.utcnow() - info['created_date']).days) >=1: # if token created date greater than (datetime seconds to datetime day) we are removing the token from collection
                information.append(info['_id'])
                mytokens.remove({"_id":{"$in": information }}) # here we are using the in operator checking the in list of objects if time is greather then (datetime seconds to datetime day)
                mytokens.update(
                {"user_id": str(user_id),"access_token":a_token},
                {
                    "$set": {"active":False}
                    }
                    )

        return Response('Logout successfully')

