from django.contrib import admin
from .models import Order, Subjects, UserEmail, MessageToWatson

admin.site.register(Order)
admin.site.register(UserEmail)
admin.site.register(MessageToWatson)
admin.site.register(Subjects)


                    
# Register your models here.
    