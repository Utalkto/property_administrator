from rest_framework import serializers, fields
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        
        

# QUERY SERIALIZERS 

class NotificationQuerySerializer(serializers.Serializer):
    
    seen = fields.BooleanField(default=False)
    send_from = fields.IntegerField(min_value=0, default=0)
    send_up_to = fields.IntegerField(min_value=1, default=20)