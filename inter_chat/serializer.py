from rest_framework import serializers, fields
from .models import Chat, ChatMessage

from register.serializers import UserSerializer


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
        
        
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        

# QUERY serializers

class ChatMessageQuerySerializer(serializers.Serializer):
    
    from_message = fields.IntegerField(min_value=0, default=0)
    up_to_message = fields.IntegerField(min_value=1, default=20)
    

class ChatQuerySerializer(serializers.Serializer):
    
    id = fields.IntegerField(min_value=0, default=0)
    all = fields.BooleanField(default=True)
        
    

    
    