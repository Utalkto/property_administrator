from properties.serializers import TenantRelatedFieldsSerializer
from tickets.serializers import SupplierGetSerializer

from .models import Chat, Conversation, Message
from rest_framework import serializers


from register.serializers import UserSerializer

class ConversationRelatedFieldsSerializer(serializers.ModelSerializer):
    
    tenant = TenantRelatedFieldsSerializer()
    supplier = SupplierGetSerializer()
    
    class Meta:
        model = Conversation
        fields = '__all__'
        
        
class ConversationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        
    
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        
        
class ChatRelatedFieldsSerializer(serializers.ModelSerializer):
    user_one = UserSerializer()
    user_two = UserSerializer()
    
    class Meta:
        model = Chat
        fields = '__all__'