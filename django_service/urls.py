
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'app/user/', include('app.urls')),
    path('',include('apptrip.urls')),

]
