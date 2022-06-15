# python

import re

# django
from rest_framework import status

from rest_framework.authtoken.views import  APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from comments.serializers import CommentAnswerSerializer, CommentRelatedFieldsSerializer, CommentSerializer

from .models import Comment

from django.utils import timezone

def check_taged_users(comment):
    users_taged = list()
    
    for m in re.finditer('@', comment):
            
        cut_comment = comment[m.start():]
        start_tag = cut_comment.find('@') + 1
        end_tag = cut_comment.find(' ')
        
        if end_tag <= 0:
            end_tag = len(cut_comment)
        
        users_taged.append(cut_comment[start_tag:end_tag])
    
    return users_taged


class CommentsAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request, client_id):
        
        comment_id = request.data.get('comment_id')
        
        print('-------------------------')
        print(comment_id)
        print('-------------------------')
        
        if comment_id is not None:
            try:
                comments = Comment.objects.filter(id=int(comment_id))
            except ValueError:
                return Response({
                    'error': 'ValueError: the value provided in the variable comment_id is not valid, it must be int'
                })
            
            if not len(comments):
                return Response({
                    'error': 'Comment.DoesNotExist: the comment with provided id does not exist'
                })
        else:
            comments = Comment.objects.filter(client=client_id)
        
        serializer = CommentRelatedFieldsSerializer(comments, many=True)
        
        return Response(serializer.data)
      
        
    def post(self, request, client_id):
        
        comment:str = request.data['comment']
        users_taged = check_taged_users(comment)
        
        # send notifications to the taged users
        request.data['client'] = client_id
        request.data['users_taged'] = users_taged
        request.data['made_by'] = request.user.id
        request.data['date_made'] = timezone.now()
        
        
        if request.data.get('is_answer'):
            serializer = CommentAnswerSerializer(data=request.data)
            request.data['answer'] = request.data['comment']
            request.data['comment'] = request.data['parent']    
        else:
            serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({
                'error': serializer.errors
            })
        
        return Response(serializer.data)
            

class CommentAnswersAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    def get(self, request, client_id):
        pass
    
    def post(self, request, client_id):
        
        answer:str = request.data.get('answer')
        users_taged = check_taged_users(answer)
        
        request.data['client'] = client_id
        request.data['users_taged'] = users_taged
        request.data['made_by'] = request.user.id
        request.data['date_made'] = timezone.now()
        
        serializer = AnswerSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
        
        
    
    
