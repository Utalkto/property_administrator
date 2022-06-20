# rest_framwork
from rest_framework import serializers

#models
from register.serializers import UserSerializer

from .models import ToDoList

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__'
        

class ToDoLitRelatedFieldsSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = ToDoList
        fields = '__all__'