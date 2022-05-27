from rest_framework import serializers
from .models import Expenses, Categories

from tickets.serializers import SupplierSerializer


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = '__all__'


class ExpensesGetSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    supplier = SupplierSerializer()
    
    
    class Meta:
        model = Expenses
        fields = '__all__'
        
        
class ExpensesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'