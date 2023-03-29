import json
import logging
from django.contrib.auth.models import User, Group
from app.serializers import UserSerializer
from django.views import View
from django.http import JsonResponse
from rest_framework import status
from django_service import settings
from django.shortcuts import get_object_or_404, get_list_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import HttpResponse


logger = logging.getLogger("django_service.service.views")

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
            if User.objects.filter(email=data.get('email')):
                logger.info("Email Already Exists")
                return JsonResponse({"message": "email already exists"},
                                    status=status.HTTP_400_BAD_REQUEST)
            User.objects.create_user(**data)
            logger.info("User created Successfully")
            return JsonResponse({"message": "user created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Exception while connect to DB %s", e)
            return JsonResponse({"message": "DB connection error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthenticateUser(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='username or email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')
        }
    ))
    def post(self, request, format=None):
        data = json.loads(request.body)
        user = authenticate(request=request, username=data["username"], password=data["password"])
        print(user)
        if user is not None:
            if user.is_active:
                user_obj = User.objects.get(Q(username__iexact=data["username"]) | Q(email__iexact=data["username"]))
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)

                
                grplist = []
                for grp in user_obj.groups.all():
                    list = {"name": grp.name}
                    grplist.append(list)

                return JsonResponse({"status": "success", "msg": "user authenticated", "username": user_obj.username, "email": user_obj.email,
                     "role": grplist[0]["name"] if grplist else '', "token": token},
                                    status=status.HTTP_200_OK)
                                   
            else:
                return JsonResponse({"status": "error", "msg": "user not active."})
        else:
            return JsonResponse({"status": "error", "msg": "The username/password specified is not valid."}, status=status.HTTP_400_BAD_REQUEST)


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


class GetAllUsers(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        API endpoint that fetch all users.
        """
        users_data = User.objects.all().order_by('-date_joined')
        user_serializer = UserSerializer(users_data, many=True, context={'request': request})
        return JsonResponse({"users": user_serializer.data})


class GetUserById(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """
        API endpoint that fetch user by id.
        """
        queryset = User.objects.filter(id=pk)
        serializer_user = UserSerializer(queryset, many=True, context={'request': request})
        return JsonResponse({"users": serializer_user.data})


class ProfileView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        data = dict()
        data['username'] = request.user.username
        data['email'] = request.user.email
        data['user_id'] = request.user.pk
        logger.info("User data %s", data)
        return Response(data)
