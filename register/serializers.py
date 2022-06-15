from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


from .models import Country, CustomUser, KumbioPlan, Organization, OrganizationClient

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class KumbioPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = KumbioPlan
        fields = '__all__'


class OrganizationGetSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    plan = KumbioPlanSerializer()
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationClient
        fields = '__all__'

class OrganizationClientGetSerializer(serializers.ModelSerializer):
    organization = OrganizationGetSerializer()
    
    class Meta:
        model = OrganizationClient
        fields = '__all__'


class UserPermissionsSerializser(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = (
            'can_delete_data',
            'can_edit_data',
            'can_add_data',
            'modules_access',
            'clients_access',
            'property_access',)
        
            
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        exclude = ('password',)