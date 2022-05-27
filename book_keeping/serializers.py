from rest_framework import serializers

from properties.serializers import UnitsSerializerProperty
from .models import BanksAccounts, Expenses, Categories

from tickets.serializers import SupplierSerializer


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categories
        fields = '__all__'


class ExpensesGetSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    supplier = SupplierSerializer()
    unit = UnitsSerializerProperty()
    
    
    class Meta:
        model = Expenses
        fields = '__all__'
        
        
class ExpensesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
        
        
        
class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BanksAccounts
        fields = '__all__'