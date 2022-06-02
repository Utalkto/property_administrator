import defusedxml
from django.db import models

# models for the foreing key 
from properties.models import Tenants
from register.models import CustomUser
from tickets.models import Suppliers


class MessageSent(models.Model):
    
    # foreign keys 
    
    tenant = models.ForeignKey(Tenants, null=True, blank=False, on_delete=models.CASCADE, default=None)
    supplier = models.ForeignKey(Suppliers, null=True, blank=False, on_delete=models.CASCADE, default=None)
    
    user = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, default=1)

    #  ------------------------------------
    #  fields
    
    
    date_time_sent = models.DateTimeField()
    
    message = models.TextField(default='')
    
    receiver = models.CharField(default='tenant', max_length=80)
    
    subject = models.CharField(max_length=120, null=True)
    sent_by = models.CharField(default='user', max_length=80)
    
    via = models.CharField(max_length=50, default='')  
    
    def __str__(self) -> str:
        return f'{self.id} - {self.via}'
    
    
    
    
    
    
