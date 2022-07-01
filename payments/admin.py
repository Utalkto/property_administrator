from django.contrib import admin

from .models import Status, UnitPayments, UnitMonthlyPayments, CurrentPaymentDate


admin.site.register(Status)
admin.site.register(UnitPayments)
admin.site.register(UnitMonthlyPayments)
admin.site.register(CurrentPaymentDate)

# Register your models here.
