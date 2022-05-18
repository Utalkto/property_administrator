from django.db import models

# models for the foreing key 
from properties.models import Tenants
from register.models import CustomUser


class MessageSent(models.Model):
    
    # foreign keys 
    
    destinatary = models.ForeignKey(Tenants, null=False, blank=False, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)

    #  ------------------------------------
    #  fields
    
    date_time_sent = models.DateTimeField()
    
    message = models.TextField(default='')
    subject = models.CharField(max_length=120, null=True)  
    
    via = models.CharField(max_length=50, default='')  
    
    
    
    
    
    
