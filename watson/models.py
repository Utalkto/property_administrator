from django.utils import timezone
from django.db import models

from uuid import uuid4
# Create your models here.

class UserEmail(models.Model):
    email = models.EmailField()


class Product(models.Model):
    
    product_id = models.CharField(primary_key=True, default=str(uuid4()), max_length=120)
    product = models.CharField(max_length=120, null=True, default=None)
    
    characteristics = models.CharField(max_length=120, null=True, default=None)
    price = models.CharField(max_length=120, null=True, default=None)
    status = models.CharField(max_length=120, null=True, default=None)
    
    ice_cream = models.CharField(max_length=120, null=True, default=None)
    extra_toppingss = models.CharField(max_length=120, null=True, default=None)
    
    drink = models.CharField(max_length=120, null=True, default=None)
    dough = models.CharField(max_length=120, null=True, default=None)
    
    email = models.EmailField(null=True, default=None)
    
    date_time_order = models.DateTimeField(default=timezone.now)
    
    
    
