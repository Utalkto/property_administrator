from properties.models import (Property, PropertyCities, PropertyCountries, PropertyType, 
                               Team, TenantType, Tenants, UnitContractType, Unit)
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
        model = PropertyType
        fields = '__all__' 


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyRelatedFieldsSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    property_type = PropertyTypeSerializer()
    
    class Meta:
        model = Property
        fields = '__all__'


class UnitPropertyRelatedSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    
    class Meta:
        model = Unit
        fields = '__all__'

class TenantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantType
        fields = '__all__'
    

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = '__all__'


class TenantRelatedFieldsSerializer(serializers.ModelSerializer):
    unit = UnitPropertyRelatedSerializer()
    tenant_type = TenantTypeSerializer()
    class Meta:
        model = Tenants
        fields = '__all__'
        
        
class TenantNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenants
        fields = ('id', 'name',)
        

class LeaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitContractType
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class UnitRelatedFieldsSerializer(serializers.ModelSerializer):
    tenants = TenantNameSerializer(many=True)
    lease_typee = LeaseTypeSerializer()
    property = PropertySerializer()
    
    class Meta:
        model = Unit
        fields = '__all__'

        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

        
        