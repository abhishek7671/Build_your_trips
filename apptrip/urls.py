from django.urls import path
from . import views


urlpatterns = [

    
    # path(r'pasttrip',views.Ptrip.as_view()),
    # path(r'pastcompletetrip',views.pasttrip.as_view()),
    # path(r'past/<str:user_id>/<str:trip_id>/', views.Past.as_view()),
    # path(r'pastuser/<str:user_id>',views.Past_User_id.as_view()),
    


    path(r'createtrip',views.Create_Travel.as_view()),
    path(r'CompleteTrip',views.CompleteTrip.as_view()),
   
    path(r'futureuser/<str:user_id>',views.Future_User_id.as_view()),
    path('future/<str:user_id>/<str:trip_id>/',views.Future.as_view()),
    

    path(r'Budgetpostcall/',views.PostcallAPI.as_view()),
    path('ExpensesAPI_tripid/<str:trip_id>/',views.ExpensesAPI.as_view()),
    path('GetCallAPI/<str:trip_id>/<str:expense_id>/',views.GetExpenseAPI.as_view()),


    path('SplitAmount',views.TotalExpensesAPI.as_view()),
    path('get-Tripid/<str:trip_id>/',views.LastExpenseDetailsAPI.as_view()),
      
]

