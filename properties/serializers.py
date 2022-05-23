from properties.models import Properties, Tenants, Units
from rest_framework import serializers


class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = '__all__'
        
        
class TenantsForUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = ('id', 'name',)
        
        
class UnitsSerializer(serializers.ModelSerializer):
    tenants = TenantsForUnitSerializer(many=True)
    
    class Meta:
        model = Units
        fields = '__all__'