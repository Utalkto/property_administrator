from django.utils import timezone
from django.db import models

from uuid import uuid4
# Create your models here.

class Subjects(models.Model):
    subject = models.TextField()


class MessageToWatson(models.Model):
    message = models.TextField()


class UserEmail(models.Model):
    email = models.EmailField()


class Order(models.Model):
    
    product = models.CharField(max_length=120, null=True, default=None)

    details = models.JSONField()
    
    status = models.CharField(max_length=120, null=True, default=None)

    email = models.EmailField(null=True, default=None)

    order_code = models.IntegerField(default=0)
    
    date_time_order = models.DateTimeField(default=timezone.now)
    
    address = models.CharField(max_length=120, null=True, default=None)

    price = models.IntegerField(default=10)

    
