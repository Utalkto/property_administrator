from django.contrib import admin
from .models import Order, Subjects, UserEmail, MessageToWatson, Calendar, CalendarAvailability

admin.site.register(Order)
admin.site.register(UserEmail)
admin.site.register(MessageToWatson)
admin.site.register(Subjects)
admin.site.register(Calendar)
admin.site.register(CalendarAvailability)


                    
# Register your models here.
    