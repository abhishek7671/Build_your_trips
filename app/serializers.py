from django.contrib.auth.models import User
from rest_framework import routers, serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from .models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = '__all__'
#         fields = ['username', 'password', 'email', 'first_name', 'last_name', 'mobile']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = [ 'username','email','password']
     

 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True,max_length=32)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "account is not activated currently"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Invalid credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "User name and password not empty"
            raise exceptions.ValidationError(msg)
        return data
    


# class UserDataSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     # Add other user data fields as needed

#     def to_representation(self, instance):
#         user = self.context['request'].user  # Get logged-in user object
#         if user.is_authenticated:  # Check if user is authenticated
#             user_data = {
#                 'username': user.username,
#                 'email': user.email,
#                 # Add other user data fields as needed
#             }
#             return user_data
#         else:
#             return {'message': 'User not authenticated'}


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import update_last_login
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['santhosh']
mycol = db["token_db"]

#-------------------------------------------------------------------------------------------------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): # for access and refresh tokens generating
    """
    Override default TokenObtainPairSerializer to use email as username field.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override default username field to use email
        self.fields['username'] = serializers.EmailField()

    def validate(self, attrs):
        # Use email to get user instance
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        mycol.insert_one({
                      "token": data,
                     })

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

