from properties.models import Properties, PropertyCities, PropertyCountries, PropertyTypes, Tenants, Units
from rest_framework import serializers


class CountryForCity(serializers.ModelSerializer):
    class Meta:
        model = PropertyCountries
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country = CountryForCity(many=False)
    class Meta:
        model = PropertyCities
        fields = '__all__'
        


class CountrySerializer(serializers.ModelSerializer):
    propertycities_set = CitySerializer(many=True)
    class Meta:
        model = PropertyCountries
        fields = '__all__' 
        
        
        
class PropertyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyTypes
        fields = '__all__' 


class PropertiesSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    property_type = PropertyTypeSerializer()
    
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
        
        
class UnitsSerializerNoTenant(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = '__all__'
        
        
        



        
        