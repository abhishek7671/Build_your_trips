import pymongo
import jwt
from rest_framework.exceptions import AuthenticationFailed
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["santhosh"]
tokens = mydb['tokens']

JWT_SECRET_KEY = 'django-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02'
JWT_ACCESS_TOKEN_EXPIRATION = 60
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'

def token_required(func):
    def inner(request, *args, **kwargs):
      
        auth_header = request.headers.get('Authorization')
        a_token = auth_header.split()[1]
        access_token = jwt.decode(a_token, JWT_SECRET_KEY, JWT_ALGORITHM)
        id =access_token['user_id']
        details = tokens.find_one({"user_id":str(id),"access_token":a_token,"active":True})
        if details:
            return func(request, *args, **kwargs)
        else:
            raise AuthenticationFailed({'Message':'Token is blacklisted'})
         
    return inner