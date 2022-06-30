# django

from django.utils import timezone


# rest_framework

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# swagger ui
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# models 
from .models import Chat, ChatMessage

# serializers
from .serializer import ChatQuerySerializer, ChatSerializer, ChatRelatedFieldsSerializer, ChatMessageSerializer



class ChatAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    @swagger_auto_schema
    def get(self, request):
        """Para obtener los mesajes enviados de manera interna
        Args:
            request (_type_): _description_
            chat_id (int): _description_
        """
        
        pass

    
    @swagger_auto_schema(
    request_body=ChatSerializer())
    def post(self, request):
        """Para cear un nuevo chat entre dos usuarios

        body_parameters:
            this (bool): this cna be null

        Returns:
            _type_: _description_
        """
        
        chat_serializer = ChatSerializer(data=request.data)
        
        if chat_serializer.is_valid():
            chat_serializer.save()
            return Response(chat_serializer.data)
        
        return Response({'error': chat_serializer.errors})


class WritingInConversationAPI(APIView):    
    
    
    @swagger_auto_schema
    def get(self, request, conversation_id:int):
        
        """Para checkear si la otra persona de la conversaction esta escribiendo

        Returns:
            _type_: _description_
        """
        
        conversation, stat = self.validate_conversation(conversation_id=conversation_id)
        
        if stat != status.HTTP_100_CONTINUE:
            return (conversation, stat)

        
        if conversation.current_writing != request.user and conversation.current_writing is not None:            
            return Response({'writing': True})
        else:
            return Response({'writing': False})
        
        
    @swagger_auto_schema
    def put(self, request, conversation_id:int):
        """Para hacer que alguien se muestre que esta escribiendo en la conversacion, 
        o mostrar como nula esa escritura
        
        body_parameters:
            writing (BooleanField): se utiliza para indicar si la psersona esta escribiendo o no
        

        Args:
            request (_type_): _description_
            conversation_id (int): el id para la conversacion cuyo estado se quiere cambiar 

        Returns:
            _type_: _description_
        """
        
        writing = request.data['writing']
        
        conversation, stat = self.validate_conversation(conversation_id=conversation_id)
        
        if stat != status.HTTP_100_CONTINUE:
            return (conversation, stat)
        
        if writing:
            conversation.current_writing = request.user
        else:
            conversation.current_writing = None
            
        conversation.save()
        
        return Response({'message': 'success'})
        
    
    def validate_conversation(self, conversation_id:int):
        
        try:
            conversation:Chat = Chat.objects.get(id=conversation_id)
            return conversation, status.HTTP_100_CONTINUE
        except Chat.DoesNotExist:
            return {'error':'Conversation.DoesNotExist: no hay conversacion con este id'}, status.HTTP_404_NOT_FOUND


class ChatMessageAPI(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    @swagger_auto_schema(
        responses={200: ChatRelatedFieldsSerializer()},
        query_serializer=ChatQuerySerializer())
    def get(self, request, chat_id:int):
        
        """Para obtener los mensajes que pertenecen a un chat
        """
        
        chat, stat = self.validate_chat(chat_id)
        
        if stat != status.HTTP_100_CONTINUE:
            return Response(chat, status=stat)

        # validando los query parameters
        qp = ChatQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        
        
        messages = ChatMessage.objects.filter(chat=chat.id).order_by('-id')[qp.data['from_message']:qp.data['up_to_message']]
        
        serializer = ChatMessageSerializer(messages, many=True)


        return Response(serializer.data)
    
    
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        'file': openapi.Schema(type=openapi.TYPE_FILE),
        'image': openapi.Schema(type=openapi.TYPE_FILE)
    },
    required=['message']),
    # --------------------------------
    responses={201: ChatMessageSerializer()},
    operation_description="this is the description testing over here")
    
    def post(self, request, conversation_id:int):
        
        conversation, stat = self.validate_chat(conversation_id)
        
        if stat != status.HTTP_100_CONTINUE:
            return Response(conversation, status=stat)
        
        
        request.data['conversation_id'] = conversation.id
        request.data['date_time_sent'] = timezone.now()
        serializer = ChatMessageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            return Response(serializer.errors)
    
    
    def validate_chat(self, conversation_id:int):
        
        try:
            conversation:Chat = Chat.objects.get(id=conversation_id)
            return conversation, status.HTTP_100_CONTINUE
        except Chat.DoesNotExist:
            return {'error':'Conversation.DoesNotExist: no hay chat con este id'}, status.HTTP_404_NOT_FOUND