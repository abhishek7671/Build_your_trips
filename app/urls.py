from django.urls import include, path
from rest_framework import routers
# from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import ChangePassword,Register,LoginView



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
   path(r'register/', Register.as_view()),
   path(r'login/', LoginView.as_view()),
   #  path(r'Pass_checker/', AuthenticateUser.as_view()),
   #  path(r'logout/', LogoutView.as_view()),
    path(r'changepassword/', ChangePassword.as_view()),
   #  path(r'getusers/', GetAllUsers.as_view()),
   #  path(r'getusersbyid/<int:pk>', GetUserById.as_view()),
   #  path(r'profile', ProfileView.as_view()),
   # #  path('pro', profile),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),




   
]