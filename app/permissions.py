import jwt
from rest_framework.permissions import IsAuthenticated
from .models import USER_details
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from bson import ObjectId
JWT_SECRET_KEY = 'django-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02'
JWT_ACCESS_TOKEN_EXPIRATION = 60
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'



class CustomIsauthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users with valid JWT tokens.
    """


    def has_permission(self, request, view):

        try:
            
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

            user = USER_details.objects.get(_id=ObjectId(payload['user_id']))
            return Response(payload)

        except (KeyError, jwt.exceptions.DecodeError, USER_details.DoesNotExist):
            raise AuthenticationFailed({'message': 'Authorization details are not provided'})