# pandas

import pandas as pd

# rest framework
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from register.models import OrganizationClient

from .extra_modules import Uploader

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# query serializers

from .queryserializers import UploaderQuerySerializer


class UploadAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    @swagger_auto_schema(
        query_serializer=UploaderQuerySerializer()
    )
    def get(self, request, client_id):
        """Regresa los campos necesarios para crear una tabla en la base de datos
        """
        
        # maybe in a future each client can have their own parameters in the database or maybe not
        client = OrganizationClient.objects.get(id=client_id)
        uploader = Uploader(request.user, client=client)
        
        qp = UploaderQuerySerializer(data=request.query_params)
        
        qp.is_valid(raise_exception=True)
        
        fields = uploader.get_neccessary_fields(table=qp.data['table'])
        
        return Response({'fields': fields})

    
    def post(self, request, client_id):
        
        """para ingresar documentos en la base de datos mediante archivos xlsx o csv
        """

        file = request.FILES['file']
        
        filename = str(file.name).split('.')[0]
        file_extension = str(file.name).split('.')[1]
        
        client = OrganizationClient.objects.get(id=client_id)
        uploader = Uploader(request.user, client)
        
        data, stat = uploader.upload_file_to_database(filename=file, file_type=file_extension, table=filename)
        
        if not stat:
            return Response({'error': data}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data)   
             

# Token 43302189e044f29f641d6305804b2b865287f098