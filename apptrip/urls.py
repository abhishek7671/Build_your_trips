from django.urls import path,include
from . import views
# from rest_framework import routers

# router = routers.SimpleRouter()
# router.register('past',views.Ptrip)
# router.register('future',views.Ftrip1, basename='Ftrip')

urlpatterns = [

    
    path('p/',views.Ptrip.as_view()),
    # path('p/<int:pk>',views.Ptrip.as_view()),
    
    
    path('past/',views.Past.as_view(),),
    path('past/<str:_id>/',views.Past.as_view()),

    
    path('f/',views.Ftrip.as_view()),
    path('CompleteTrip/',views.CompleteTrip.as_view()),
    
    path('future/',views.Future.as_view()),
    path('future/<str:_id>/',views.Future.as_view()),

    # path('trips/',views.TripCreateView.as_view()),
    path('trips/<str:trip_id>/', views.TripView.as_view(), name='trip-detail'),

#    path('general/',views. GeneralTrip.as_view()),
#    path('natural/',views.NaturalTrip.as_view()),
#    path('natural/<str:_id>/',views.NaturalTrip.as_view()),








    # path('',include(router.urls)),
    # path('',include(router.urls)),
    

    # path('ptrip/',views.ptrip),
    # path('abhi/',views.Ptrip.as_view()),
    # path('abhi/<str:_id>/',views.Abhi.as_view()),
    # # path('abhi',views.abhi),
    # path('get/<int:pk>',views.GetView.as_view()),
    # path('create',views.create),
    # path('P1/<int:pk>',views.Ptrip1.as_view()),

    # path('ft/',views.Ftrip.as_view()),
    # path('F/',views.FutureCreate.as_view()),
    # path('F1/<int:pk>',views.Ftrip1.as_view()),


]