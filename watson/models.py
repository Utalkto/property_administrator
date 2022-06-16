from django.utils import timezone
from django.db import models

# Create your models here.

class Subjects(models.Model):
    subject = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.id} - {self.subject}'


class MessageToWatson(models.Model):
    message = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.id}'


class UserEmail(models.Model):
    email = models.EmailField()
    
    def __str__(self) -> str:
        return f'{self.id} - {self.email}'


class Order(models.Model):
    
    product = models.CharField(max_length=120, null=True, default=None)

    details = models.JSONField()
    
    status = models.CharField(max_length=120, null=True, default=None)

    email = models.EmailField(null=True, default=None)

    order_code = models.IntegerField(default=0)
    
    date_time_order = models.DateTimeField(default=timezone.now)
    
    address = models.CharField(max_length=120, null=True, default=None)

    price = models.IntegerField(default=10)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.product}'


class Calendar(models.Model):
    name = models.CharField(max_length=120)
    
    
class CalendarAvailability(models.Model):
    calendar = models.ForeignKey(Calendar, null=False, blank=False, on_delete=models.CASCADE)
    
    # ---------------------------------------
    # fields
    
    date = models.DateField()
    hour = models.CharField(max_length=120)
    email_of_attendee = models.EmailField(null=True, default=None)
    duration = models.CharField(max_length=120)
    
    
    def save(self, *args, **kwargs):
        if self.email_of_attendee == 'email@none.com':
            self.email_of_attendee = None
            
        super(CalendarAvailability, self).save(*args, **kwargs)
    
