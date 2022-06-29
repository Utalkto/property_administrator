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
    
    
class Chat(models.Model):
    
    """Modelo utilizado para las conversaciones internas de la aplicacion
    """
    
    user_one = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='user_two')
    
    last_message = models.TextField()
    last_message_sent_by = models.IntegerField() # 0 for user_one and 1 for user_two
    
    current_writing = models.ForeignKey(CustomUser, null=True, default=None, on_delete=models.CASCADE, related_name='current_writing')
    


class ChatMessage(models.Model):
    
    conversation = models.ForeignKey(Chat, null=False, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='sent_by')
    
    
    date_time_sent = models.DateTimeField()
    
    file = models.FileField(null=True, default=None)
    
    image = models.ImageField(upload_to='chat-images', null=True, default=None)
    
    message = models.TextField(null=True, default=None)
    
    
    
    
