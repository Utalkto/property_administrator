from .models import MessageSent
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageSent
        fields = '__all__'