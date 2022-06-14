from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from app_modules.send_email import SendEmail

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from comments.serializers import CommentRelatedFieldsSerializer

from .models import Comment


class CommentsAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def get(self, request, client_id):
        
        
        comment_id = request.GET.get('comment_id')
        
        if comment_id is not None:
            
            try:
                comments = Comment.objects.filter(id=int(comment_id))
            except ValueError:
                return Response({
                    'error': 'ValueError: the value provided in the variable comment_id is not valid, it must be int'
                })
            
        else:
            comments = Comment.objects.filter(client=client_id)
        
        serializer = CommentRelatedFieldsSerializer(comments, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, client_id):
        pass
    
