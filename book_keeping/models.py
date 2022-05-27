from django.db import models

from properties.models import Units, Tenants
from tickets.models import Suppliers


class BanksAccounts(models.Model):
    # foreign keys
   
    # ------------------------------------
    # fields
    amount_paid = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
   
    bank = models.CharField(max_length=100)
    building_if_is_mortgage = models.CharField(max_length=100)
    balance = models.CharField(max_length=100)
   
    city = models.CharField(max_length=100)
    credit_amount_initial = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
   
    interest_rate = models.CharField(max_length=50)
    interest_payment = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
   
    last_4_digits_of_account = models.CharField(max_length=4)
   
    monthly_payment = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
   
    def __str__(self) -> str:
        return self.amount_paid


class Categories(models.Model):
    name = models.CharField(max_length=60)


class Expenses(models.Model):
    # foreign keys
    unit = models.ForeignKey(Units, default =None, null=True, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, default=None, null=False, blank=False, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, default=None, null=True, on_delete=models.CASCADE)

    # --------------------------------
    # fields
   
    account = models.TextField()
    amount = models.IntegerField(default=0)
   
    date = models.DateField()
    description = models.TextField(null=True)
   
    kilometers_traveled = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=None)
   
    # ------------------------
    payment_method = models.CharField(max_length=100)
   
    rate_per_kilometer = models.CharField(max_length=100, null=True, default=None)
    receipt_number = models.IntegerField(default=0)
   
    sub_account = models.TextField(null=True, default=None)
   
    def __str__(self) -> str:
        return self.categories.name
   
   
class PaymentRent(models.Model):
    # foreign keys
   
    tenant = models.ForeignKey(Tenants, null=False, blank=False ,on_delete=models.CASCADE)
    unit = models.ForeignKey(Units, null=False, blank=False ,on_delete=models.CASCADE)

    # -----------------------------
    # field
   
    account = models.TextField()
   
    date_payment = models.DateField(null=True)
    debt = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
   
    month_paid = models.CharField(max_length=20, default='')
   
    payment = models.DecimalField(max_digits=19, decimal_places=2, default=0, null=False)
    pending_payment_date = models.DateField(null=True)
   
    status = models.IntegerField()
    sub_account = models.TextField()
   
    def __str__(self) -> str:
        return self.account
