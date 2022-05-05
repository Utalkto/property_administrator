from rest_framework import serializers
from .models import Candidate

class FormForCandiatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
