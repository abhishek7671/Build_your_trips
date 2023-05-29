
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.blacklist.views import BlacklistView
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('',include('apptrip.urls')),
    path("auth/logout/", BlacklistView.as_view({"post": "create"}))

]
