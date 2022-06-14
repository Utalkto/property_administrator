from atexit import register
from rest_framework import serializers
from .models import Comment, CommentAnswer

from register.serializers import UserSerializer, OrganizationClientSerializer

class CommentRelatedFieldsSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    client = OrganizationClientSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        

class AnswerSerializer(serializers.ModelSerializer):
    
    comment = CommentSerializer()
    user = UserSerializer()
    
    class Meta:
        model = Comment
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentAnswer
        fields = '__all__'