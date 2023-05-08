from django.urls import path
from . import views


urlpatterns = [

    
    path('p/',views.Ptrip.as_view()),
    # path('p/<int:pk>',views.Ptrip.as_view()),
    
    
    path('past/',views.Past.as_view(),),
    path('past/<str:_id>/',views.Past.as_view()),

    
    path('create/',views.Create_Travel.as_view()),
    path('CompleteTrip/',views.CompleteTrip.as_view()),
    
    path('future/',views.Future.as_view()),
    path('future/<str:_id>/',views.Future.as_view()),

]