from atexit import register
from rest_framework import serializers
from .models import Comment, CommentAnswer

from register.serializers import UserSerializer, OrganizationClientSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        

class CommentAnswerRelatedFeildsSerializer(serializers.ModelSerializer):
    comment = CommentSerializer()
    user = UserSerializer()
    
    class Meta:
        model = CommentAnswer
        fields = '__all__'


class CommentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentAnswer
        fields = '__all__'
        
        
class CommentRelatedFieldsSerializer(serializers.ModelSerializer):
    commentanswer_set = CommentAnswerSerializer(many=True)
    made_by = UserSerializer()
    client = OrganizationClientSerializer()

    class Meta:
        model = Comment
        fields = '__all__'