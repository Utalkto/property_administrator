# rest_framework
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from app_modules.permission import get_propeties_with_access, user_has_access

from .serializers import FormSerializer
from .query_serializer import FormQuerySerializer
from .models import Form



class FormsAPI(APIView):
    # permission_classes = (IsAuthenticated,) 
    # authentication_classes = (TokenAuthentication,) 
    
    @swagger_auto_schema()
    def get(self, request, client_id):
        
        qp = FormQuerySerializer(request.query_params)
        qp.is_valid(raise_exception=True)
        qp = qp.data
        
        if client_id == 'all':
            
            if qp['unit_id']:
                properties_with_access = get_propeties_with_access(request.user)
                forms = Form.objects.filter(unit__property__in=properties_with_access)
            
            else:
                clients = request.user.access_clients.keys()
                forms = Form.objects.filter(client__in=clients)
        
        else:
            
            try:
                client_id = (client_id)
            except ValueError:
                return Response({
                    'error': 'client_id debe ser entero or set to "all" para traer todos los formularios \
                        linkeados a ese client'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            
            if not user_has_access(request.user, client_id=client_id):
                return Response({
                    'error': 'User has not access to this client'
                }, status=status.HTTP_403_FORBIDDEN)
       

            forms = Form.objects.filter(client_id=client_id)
        
        serializer = FormSerializer(forms, many=True)
        
        return Response(serializer.data)
        

    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'form_fields': openapi.Schema(type=openapi.TYPE_OBJECT),
            'unit': openapi.Schema(type=openapi.TYPE_INTEGER, default=None),
        },
        required=['name', 'form_fields']),
        responses={200: FormSerializer()}
    )
    def post(self, request, client_id):
        
        request.data['created_by'] = 1
        request.data['client'] = client_id
        
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
    
    
    
        
    @swagger_auto_schema()
    def put(self, request, client_id):
        pass
    
    
    @swagger_auto_schema()
    def delete(self, request, client_id):
        pass




# Token 43302189e044f29f641d6305804b2b865287f098