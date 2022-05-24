from django.contrib import admin
from .models import Properties, TenantType, Units, Tenants, Links, PropertyCountries, PropertyCities, PropertyTypes, UnitTypes

admin.site.register(Properties)
admin.site.register(Units)
admin.site.register(Tenants)
admin.site.register(Links)
admin.site.register(PropertyCountries)
admin.site.register(PropertyCities)
admin.site.register(PropertyTypes)
admin.site.register(UnitTypes)
admin.site.register(TenantType)



