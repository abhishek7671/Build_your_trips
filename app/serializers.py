from rest_framework import  serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from .models import USER_details


 
class USER_Serializer(serializers.ModelSerializer):
  class Meta:
    model = USER_details
    fields = ['email','password','date_joined']     

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
    




