from django.contrib import admin
from .models import CustomUser, UserCountries, UserCities, UserRoles, UserPlans 

admin.site.register(CustomUser)
admin.site.register(UserCountries)
admin.site.register(UserCities)
admin.site.register(UserRoles)
admin.site.register(UserPlans)
