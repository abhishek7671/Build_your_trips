from django.urls import path
from . import views


urlpatterns = [

    
    path(r'p',views.Ptrip.as_view()),
    # path('p/<int:pk>',views.Ptrip.as_view()),
    
    
    path(r'past/',views.Past.as_view(),),
    path(r'past/<str:_id>/',views.Past.as_view()),

    
    path(r'create/',views.Create_Travel.as_view()),
    path(r'CompleteTrip/',views.CompleteTrip.as_view()),
    
    path(r'future/',views.Future.as_view()),
    path(r'future/<str:_id>/',views.Future.as_view()),

]