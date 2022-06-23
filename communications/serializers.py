from properties.serializers import TenantRelatedFieldsSerializer
from tickets.serializers import SupplierGetSerializer

from .models import Conversation, Message
from rest_framework import serializers


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
        
    
