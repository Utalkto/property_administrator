from .models import (Ticket, TicketAppoinment, TicketType, TicketPriority, 
                     TicketComments, Suppliers, SupplierWorkArea)
from rest_framework import serializers


from properties.serializers import CitySerializer

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


class WorkAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierWorkArea
        fields = '__all__'


class SupplierGetSerializer(serializers.ModelSerializer):
    work_area = WorkAreaSerializer()
    city = CitySerializer()
    class Meta:
        model = Suppliers
        fields = '__all__'
  
        
class SupplierPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'