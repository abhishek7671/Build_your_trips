from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'pViewset',views.Ptrip)
router.register(r'fViewset',views.Ftrip1, basename='Ftrip')
# router.register('f/<int:pk>', views.Ftrip1)

urlpatterns = [
    
    path('',include(router.urls)),
    path('',include(router.urls)),
    

    path('ptrip/',views.ptrip),
    # path('get/<int:pk>',views.GetView.as_view()),
    # path('ptrip/<int:pk>',views.ptrip),
    # path('ftrip',views.ftrip),
    



    # path('P1/<int:pk>',views.Ptrip1.as_view()),

    # path('ft/',views.Ftrip.as_view()),
    # path('F/',views.FutureCreate.as_view()),
    # path('F1/<int:pk>',views.Ftrip1.as_view()),


]