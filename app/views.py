from django.conf import settings
import jwt
from datetime import timedelta,datetime
import json
from app.serializers import  USER_Serializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from .models import USER_details
from .backend import EmailBackend
from rest_framework.generics import CreateAPIView
from app.permissions import CustomIsauthenticated
from django.core.mail import EmailMessage
from app.authentication import JWTAuthentication
from pymongo import MongoClient
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient['santhosh']
mycol3 = mydb['app_user_details']
tokens=mydb['tokens']

import logging
logger = logging.getLogger('custom_logger')
# logger = logging.getLogger('django')
# logger = logging.getLogger("django_service.service.views")



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
        try:
            serializer = USER_Serializer(data=json.loads(request.body))
            if not serializer.is_valid():
                logger.error("Invalid serializer data")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            password = data['password']
            hashed_password = make_password(password)
            email = data['email'] 
            existing_user = USER_details.objects.filter(email=email).first()
            if existing_user is not None:
                logger.warning('Email already exists')
                return JsonResponse({'Message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(password=hashed_password)
                logger.info('User created successfully')
                return JsonResponse({'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error('Internal server error: %s', str(e))
            return JsonResponse({'Message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email', None)
            password = data.get('password', None)

            missing_fields = [field for field in ['email', 'password'] if not data.get(field)]
            if missing_fields:
                return Response({'error': f"Missing required field(s): {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

            user = EmailBackend.authenticate(self, request, username=email, password=password)

            if user is not None:
                token = get_token_for_user(user)
                access_token = token['access']
                refresh_token = token['refresh']
                tokens.insert_one({
                    "user_id": str(user._id),
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "active": True,
                    "created_date": datetime.utcnow()
                })
                logger.info("User successfully authenticated")
                return Response({
                    "status": "success",
                    "msg": "User successfully authenticated",
                    "token": token,
                    "user_id": str(user._id),
                })
            else:
                logger.warning(f"Invalid authentication attempt for email: {email}")
                return JsonResponse({"message": "Invalid email or password"})
        except ValueError as e:
            logger.error("An error occurred during login: " + str(e))
            return JsonResponse({"message": "An error occurred during login: " + str(e)})




class ChangePassword(CreateAPIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            oldpassword = data.get('password')
            newpassword = data.get('newpassword')

            missing_fields = [field for field in ['email', 'password', 'newpassword'] if not data.get(field)]

            if missing_fields:
                return Response({'error': f"Missing required field(s): {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

            user_obj = USER_details.objects.filter(email=email).first()

            if not user_obj:
                logger.error(f"User not found for email: {email}")
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            if not check_password(oldpassword, user_obj.password):
                logger.error(f"Invalid old password for user with email: {email}")
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            user_obj.password = make_password(newpassword)
            user_obj.save()

            logger.info("Password changed successfully for user with email")
            return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred while changing password.")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

import secrets 
def generate_otp(length=6):
        """Generates a random OTP of the specified length."""
        return secrets.token_hex(length // 2 + 1)[:length]


class ForgotPassword(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data.get("email")
            missing_fields = [field for field in ['email'] if not data.get(field)]
            
            if missing_fields:
                return Response({'error': f"Missing required field(s): {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

            user_obj = USER_details.objects.filter(email=email).first()
            if not user_obj:
                return Response({'error': 'Email doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)

            otp = generate_otp()
            hashed_password = make_password(otp)
            mycol3.update(
                {"email": email},
                {"$set": {"password": hashed_password}}
            )
            email_msg = EmailMessage(
                'Email Details',
                f"RESET PASSWORD \n Hey there!\n It looks like you are trying to reset your password.\n\nYOUR NEW LOGIN DETAILS:\n password: {otp}\n Email: {email}",
                settings.EMAIL_HOST_USER,
                [email],
            )
            email_msg.send(fail_silently=True)
            logger.info('password generated successfully')
            return Response({"message": "New password generated successfully and sent to your respective email address"})

        except Exception as e:
            logger.critical("An error occurred while processing the forgot password request.")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class LogoutAll(APIView):
    permission_classes = [CustomIsauthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            user_id = request.user._id
            auth_header = request.headers.get('Authorization')
            a_token = auth_header.split()[1]
            user_data = tokens.find({})

            information = []
            for info in user_data:
                if ((datetime.utcnow() - info['created_date']).days) >= 1:
                    information.append(info['_id'])
            logger.debug("Tokens to be removed: %s", information)
            tokens.remove({"_id": {"$in": information}})

            tokens.update(
                {"user_id": str(user_id), "access_token": a_token},
                {"$set": {"active": False}}
            )
            logger.info('Logout Successfully')
            return Response('Logout successful')
        
        except Exception as e:
            logger.error("An error occurred during logout: %s", str(e))
            return Response('An error occurred during logout', status=status.HTTP_500_INTERNAL_SERVER_ERROR)



