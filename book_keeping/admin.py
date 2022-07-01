from django.contrib import admin
from .models import Expenses, BanksAccounts, Categories, PaymentRent

admin.site.register(Expenses)
admin.site.register(BanksAccounts)
admin.site.register(Categories)
admin.site.register(PaymentRent)

