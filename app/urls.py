from django.urls import path
from .views import  Register,LoginView,ChangePassword,ForgotPassword,LogoutAll



urlpatterns = [

   path(r'register',Register.as_view(),name='register'),
   path(r'login',LoginView.as_view(),name='register'),
   path('changepassword',ChangePassword.as_view()),
   path('forgotpassword',ForgotPassword.as_view()),
   path('logout',LogoutAll.as_view()),

    
]
