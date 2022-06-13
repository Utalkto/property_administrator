from rest_framework import serializers
from .models import Candidate

from properties.serializers import UnitsSerializerGet


class CandiatesGetSerializer(serializers.ModelSerializer):
    unit = UnitsSerializerGet()
    class Meta:
        model = Candidate
        fields = '__all__'


class CandiatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

    
        # exclude = ['user']