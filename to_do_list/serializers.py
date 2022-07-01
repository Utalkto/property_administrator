# rest_framwork
from rest_framework import serializers

#models
from register.serializers import UserSerializer

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        

class TaskRelatedFieldsSerializer(serializers.ModelSerializer):
    to_do_listowner = UserSerializer()
    class Meta:
        model = Task
        fields = '__all__'