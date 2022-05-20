from django.db import models

from register.models import CustomUser
from properties.models import Units


class UnitPayments(models.Model):
    # foreing keys 
    Unit = models.ForeignKey(Units, null=False, blank=False, on_delete=models.CASCADE)
    # ------------------------------------------------
    # fields 
    
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=70)
    payment_amount = models.DecimalField(decimal_places=2, max_digits=6)
    
    reference_code = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('payment_date', )
    
    
    
class UserPayments(models.Model):
    # foreing keys 
    user = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    # ------------------------------------------------
    # fields 
    
    next_due_date = models.DateField() 
    
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=70)
    payment_amount = models.DecimalField(decimal_places=2, max_digits=6)
    plan_paid = models.CharField(max_length=70)
    
    class Meta:
        ordering = ('payment_date', )
    