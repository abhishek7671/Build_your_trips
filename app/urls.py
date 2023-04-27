from django.urls import include, path
from rest_framework import routers
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import  CreateUser,ChangePassword, CustomTokenObtainPairView,LogoutAllView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



from .views import CreateUser,ChangePassword, CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
   TokenObtainPairView,
   TokenRefreshView,
)






schema_view = get_schema_view(
   openapi.Info(
      title="User API",
      default_version='v1',
      description="User related all API's",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
   path(r'create_user/',CreateUser.as_view()),
   # path('agent/',Agent_signup.as_view()),
   # path('user/', views.user_list),
   #  path(r'sign_up/', Signup.as_view()),
   #  path(r'Pass_checker/', AuthenticateUser.as_view()),
   # path(r'logout/',CustomLogoutView.as_view()),
   path(r'logout/',LogoutAllView.as_view()),
   # path(r'logout/',LogoutAPIView.as_view()),
   path(r'changepassword/',ChangePassword.as_view()),
   #  path(r'getusers/', GetAllUsers.as_view()),
   #  path(r'getusersbyid/<int:pk>', GetUserById.as_view()),
   #  path(r'profile', ProfileView.as_view()),
   # #  path('pro', profile),
   path(r'swagger/',schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path(r'redoc/',schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),



   path(r'token/',CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
   path(r'token/refreshh/',TokenRefreshView.as_view(), name='token_refresh'),

   
]