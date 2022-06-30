from django.db import models
from register.models import CustomUser

from register.models import OrganizationClient

class Chat(models.Model):
    
    """Modelo utilizado para las conversaciones internas de la aplicacion
    """
    
    client = models.ForeignKey(OrganizationClient, null=False, default=1, on_delete=models.CASCADE, related_name='chats')
    
    user_one = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='user_two')
    
    last_message = models.TextField(null=True, default=None)
    last_message_sent_by = models.IntegerField(null=True, default=None) # 0 for user_one and 1 for user_two # this can be deprecated
    last_message_sent_date = models.DateTimeField(null=True, default=None)
    
    current_writing = models.ForeignKey(CustomUser, null=True, default=None, on_delete=models.CASCADE, related_name='current_writing')


class ChatMessage(models.Model):
    
    chat = models.ForeignKey(Chat, null=False, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='sent_by')
    
    date_time_sent = models.DateTimeField()
    
    file = models.FileField(upload_to='chat/files/chat-files', null=True, default=None)
    
    image = models.ImageField(upload_to='chat/files/chat-images', null=True, default=None)
    
    message = models.TextField(null=True, default=None)
