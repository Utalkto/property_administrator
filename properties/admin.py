from django.contrib import admin
from .models import (Team, Property, TenantType, Unit, Tenants, Links, PropertyCountries, 
                     PropertyCities, PropertyType, UnitType, UnitContractType)

admin.site.register(Team)
admin.site.register(Property)
admin.site.register(Unit)
admin.site.register(Tenants)
admin.site.register(Links)
admin.site.register(PropertyCountries)
admin.site.register(PropertyCities) 
admin.site.register(PropertyType)
admin.site.register(UnitType)
admin.site.register(TenantType)
admin.site.register(UnitContractType)



