from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()

from .models import Country, CustomUser, KumbioPlan, Organization, OrganizationClient


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
            'clients_access',)
        
            
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        exclude = ('password',)


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            
            # this organization can be None? No, the organizations will be created by us
            organization=validated_data['organization'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ( "id", "email", "username", "password", "organization")