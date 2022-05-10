from django.contrib import admin
from .models import Properties, Units, Tenants, Links

admin.site.register(Properties)
admin.site.register(Units)
admin.site.register(Tenants)
admin.site.register(Links)

# Register your models here.
