from django.contrib import admin
from .models import PastTravelledTrips, FutureTrips,Contributor


admin.site.register(PastTravelledTrips)
admin.site.register(FutureTrips)
admin.site.register(Contributor)
# admin.site.register(Budget)
