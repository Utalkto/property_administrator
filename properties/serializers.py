from properties.models import Properties, PropertyCities, PropertyCountries, PropertyTypes, Team, TenantType, Tenants, Units
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


class PropertiesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'


class PropertiesSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    property_type = PropertyTypeSerializer()
    
    class Meta:
        model = Properties
        fields = '__all__'


class TenantTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TenantType
        fields = '__all__'
    

class TenantSerializer(serializers.ModelSerializer):
    
    tenant_type = TenantTypeSerializer()
    
    class Meta:
        model = Tenants
        fields = '__all__'
        
        
class TenantsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = ('id', 'name',)
        
        
class UnitsSerializer(serializers.ModelSerializer):
    tenants = TenantsNameSerializer(many=True)
    
    class Meta:
        model = Units
        fields = '__all__'
        
        
class UnitsSerializerNoTenant(serializers.ModelSerializer):
    # property = PropertiesSerializer()
    class Meta:
        model = Units
        fields = '__all__'
        

class UnitsSerializerProperty(serializers.ModelSerializer):
    property = PropertiesSerializer()
    class Meta:
        model = Units
        fields = '__all__'
        

class TeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Team
        fields = '__all__'

        
        