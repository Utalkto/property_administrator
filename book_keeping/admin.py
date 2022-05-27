from django.contrib import admin
from .models import Expenses, BanksAccounts, Categories

admin.site.register(Expenses)
admin.site.register(BanksAccounts)
admin.site.register(Categories)

