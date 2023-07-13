from django.urls import path
from . import views


urlpatterns = [


    
    path('createtrip',views.Create_Travel.as_view()),
    path('CompleteTrip',views.CompleteTrip.as_view()),
   
    path('futureuser/<str:user_id>/',views.Future_User_id.as_view()),

    path('gettrip/<str:email>/',views.GetTripDetails.as_view()),
    path('future/<str:trip_id>/',views.Future.as_view()),
    

    path('Budgetpostcall/',views.PostcallAPI.as_view()),
    path('ExpensesAPI_tripid/<str:trip_id>/',views.ExpensesAPI.as_view()),
    path('GetCallAPI/<str:trip_id>/<str:expense_id>/',views.GetExpenseAPI.as_view()),


    path('SplitAmount',views.TotalExpensesAPI.as_view()),
    path('get-Tripid/<str:trip_id>/',views.LastExpenseDetailsAPI.as_view()),
      
]

