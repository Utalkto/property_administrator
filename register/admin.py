from django.contrib import admin
from .models import (CustomUser,  Country, City, UserRoles, KumbioPlan, 
                     Organization, OrganizationClient, KumbioPlanPermission)

admin.site.register(Organization)
admin.site.register(CustomUser)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(UserRoles)
admin.site.register(KumbioPlan)
admin.site.register(OrganizationClient)
admin.site.register(KumbioPlanPermission)
