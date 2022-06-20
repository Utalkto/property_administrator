# rest_framework
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema

from register.models import Organization

# models 
from .models import Log
from logs.serializers import LogRelatedDataSerializer, LogSerializer
# modules created for the app
from app_modules.send_email import SendEmail


class LogAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    @swagger_auto_schema(
    responses={200: LogSerializer()})
    def get(self, request,  organization_id):
        
        """Devuelve los ultimos logs de un cliente de una organizacion
        
        path parameters:
            organization_id: bueno papá, si no sabes que va aquí ya me dirás tú, un beso
        
        query paramerts:
            
            client_id (int) (required): regresa los logs asociados a ese cliente, set to "all" para devolver todos logs
            asociados a todos los clientes de una organizacion
            
            logs (int) (required): regresa los ultimo n logs, set to "all" para devolver todos los logs que una hay 
            asociados al cliente dado
        """


        try:
            Organization.objects.get(id=organization_id)
        except:
            return Response({'error': 'Organization.DoesNotExist'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            client_id = request.GET['client_id']
            number_of_logs = request.GET['logs']
        except:
            return Response({'error': 'KeyError: client_id y logs debe ser dada'})
        
        
        if client_id == 'all':
            if number_of_logs == 'all':
                
                logs = Log.objects.filter(client__organization=organization_id)
                
            else:
                try: number_of_logs = int(number_of_logs)
                except: 
                    return Response({
                        'error': 'ValueError: logs debe ser int o debe ser puesta como all para devolver todos los logs'
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                logs = Log.objects.filter(client__organization=organization_id).order_by('-id')[:number_of_logs]
                
        else:
            try: client_id = int(client_id)
            except: 
                return Response({
                    'error': 'ValueError: client_id debe ser int o debe ser puesta como all para devolver todos los logs'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                
            if number_of_logs == 'all':
                logs = Log.objects.filter(client=client_id)
                
            else:
                try: number_of_logs = int(number_of_logs)
                except: 
                    return Response({
                        'error': 'ValueError: logs debe ser int o debe ser puesta como all para devolver todos los logs'
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                logs = Log.objects.filter(client=client_id).order_by('-id')[:number_of_logs]

        log_serializer = LogRelatedDataSerializer(logs)
        
        return Response(log_serializer.data)
        
        
