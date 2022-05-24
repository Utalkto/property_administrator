from .models import Ticket, TicketAppoinment, TicketType, TicketPriority, TicketComments
from rest_framework import serializers


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'
        
        
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
     
        
class TicketPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPriority
        fields = '__all__'
   
        
class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComments
        fields = '__all__'
        
        
class TicketAppoinmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAppoinment
        fields = '__all__'