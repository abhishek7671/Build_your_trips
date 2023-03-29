from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'p',views.Ptrip)
router.register(r'f',views.Ftrip1, basename='Ftrip')

urlpatterns = [
     
    # path('P/',views.Ptrip.as_view()),
    path('ptrip/',views.ptrip),
    path('',include(router.urls)),
    path('',include(router.urls)),
    
    path('P1/<int:pk>',views.Ptrip1.as_view()),
    path('f/',views.Ftrip.as_view()),
    # path('ft/<int:pk>',views.Ftrip1.as_view()),
    # path('pro',views.Entry.as_view()),
    # path('def/',views.ftrip),
    # path('cre',views.create),
    

    # path('F/',views.FutureCreate.as_view()),
    # path('F1/<int:pk>',views.Ftrip1.as_view()),


]