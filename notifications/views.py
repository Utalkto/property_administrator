# django
from django.utils import timezone

# rest_framework

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification


# serializers

from .serializers import NotificationSerializer, NotificationQuerySerializer

# same app modules 

from .extra_modules import create_notification

from app_modules.permission import user_has_access
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class NotificationAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    @swagger_auto_schema(
        query_serializer=NotificationQuerySerializer(), 
        operation_description="retorna la lista de notificaciones que pertenecen a un usuario")
    def get(self, request):
        
        
        query_parameters = NotificationQuerySerializer(data=request.query_params)
        query_parameters.is_valid(raise_exception=True)

        notifications = Notification.objects.filter(user=request.user.id, seen=query_parameters['seen']).order_by('-id') \
        [query_parameters['send_from']:query_parameters['send_up_to']]
        
        serializer = NotificationSerializer(notifications, many=True)
        
        
        return Response(serializer.data)
    
    
    @swagger_auto_schema(
        operation_description="set seen = True",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
        'notifications': openapi.Schema(type=openapi.TYPE_ARRAY, 
                                        description="una lista de las notifcaciones que quieren modificar")
    },
    required=['notifications']),
    )
    def put(self, request):
        
        list_of_notifications = request.data['notifications']
        list_of_objects = list()
        
        for notification_id in list_of_notifications:
            
            notification:Notification = Notification.objects.get(id=int(notification_id))
            notification.seen = True
            
            list_of_objects.append(notification)
            notification.save()
            
        
        serializer = NotificationSerializer(list_of_objects, many=True)

        return Response(serializer.data)
            
            
            
        