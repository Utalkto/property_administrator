from django.db import models

from register.models import CustomUser
from properties.models import Tenants, Units

class Status(models.Model):
    name = models.CharField(max_length=50, default= '')
    
    def __str__(self) -> str:
        return self.name


class UnitPayments(models.Model):
    # foreing keys 
    unit = models.ForeignKey(Units, null=False, blank=False, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, null=False, blank=False, on_delete=models.CASCADE)
    
    status = models.ForeignKey(Status, null=False, blank=False, on_delete=models.CASCADE)
    # ------------------------------------------------
    # fields 
    
    comments = models.CharField(max_length=120, default='')
        
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=70)
    payment_amount = models.DecimalField(decimal_places=2, max_digits=6)
    
    reference_code = models.CharField(max_length=100)

    # field to add to db    
    month = models.CharField(max_length=120, default='')
    
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
    