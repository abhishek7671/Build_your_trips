from django.urls import path
from . import views


urlpatterns = [

    
    path(r'past',views.Ptrip.as_view()),
    path(r'p',views.pasttrip.as_view()),

    path('past/<str:user_id>/<str:trip_id>/', views.Past.as_view()),
    # path(r'get/<str:pk>',views.Past.as_view()),
    
    # path('trips', views.TripDetailView.as_view()),
    # path('trips/<str:trip_id>/', views.TripDetailView.as_view()),



    path(r'create/',views.Create_Travel.as_view()),
    path(r'CompleteTrip/',views.CompleteTrip.as_view()),
    

    path(r'future/<str:user_id>/<str:trip_id>/',views.Future.as_view()),
    # path(r'future/<str:_id>/',views.Future.as_view()),

]