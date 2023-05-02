from django.contrib.auth.models import User
from rest_framework import routers, serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from .models import User, USER_details


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         # fields = '__all__'
#         fields = ['username', 'password', 'email', 'first_name', 'last_name', 'mobile']
class USER_Serializer(serializers.ModelSerializer):
    class Meta:
        model = USER_details
        fields = ['email','password','usertype','date_joined']
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



#-------------------------------------------------------------------------------------------------------------------------------------------------


