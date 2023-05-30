from django.urls import include, path
from rest_framework import routers
from .views import  Register,LoginView,ChangePassword,ForgotPassword,LogoutView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

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

   path(r'register',Register.as_view(),name='register'),
   path(r'login',LoginView.as_view(),name='register'),
   path('changepassword',ChangePassword.as_view()),
   path('forgotpassword',ForgotPassword.as_view()),
   path('logout',LogoutView.as_view()),

    
]
