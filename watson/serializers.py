from rest_framework import serializers
from .models import CalendarAvailability, Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CalendarAvailabilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CalendarAvailability
        fields = '__all__'