from django.db import models

# models for the foreing key 
from properties.models import Tenants
from register.models import CustomUser, OrganizationClient
from tickets.models import Suppliers


class Conversation(models.Model):
    client = models.ForeignKey(OrganizationClient, null=False, on_delete=models.CASCADE)
    
    tenant = models.ForeignKey(Tenants, null=True, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, null=True, on_delete=models.CASCADE)
    
    last_message = models.TextField(default='')
    last_message_sent_by_user = models.BooleanField(default=False)
    
    def save(self, **kwargs):
        
        if self.supplier == 33:
            self.supplier = None
        
        if self.last_message == 'None':
            self.last_message = ''
        
        super().save(**kwargs)
    

class Message(models.Model):
    
    # foreign keys 
    
    conversation = models.ForeignKey(Conversation, null=True, on_delete=models.CASCADE, default=None)
    sent_by_user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, default=None)
    

    #  ---------------------------------------------------------------------------
    #  fields
    
    date_time_sent = models.DateTimeField()
    
    message = models.TextField(default='')
    
    subject = models.CharField(max_length=120, null=True)
    
    via = models.CharField(max_length=50, default='')  
    
    unkonwn_email = models.EmailField(null=True, default=None)
    unkonwn_phone = models.CharField(max_length=120, null=True, default=None)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.via}'
    
