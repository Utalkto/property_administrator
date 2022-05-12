from rest_framework import serializers
from .models import Candidate

class CandiatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

    
        # exclude = ['user']