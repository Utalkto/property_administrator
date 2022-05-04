from django.contrib import admin
from .models import Properties, Units, Tenants

admin.site.register(Properties)
admin.site.register(Units)
admin.site.register(Tenants)

# Register your models here.
