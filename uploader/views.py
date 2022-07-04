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

class UploadAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    def post(self, request, client_id):
        
        """para ingresas documentos en la base de datos mediante archo xlsx o csv
        """

        file = request.FILES['property']
        
        filename = str(file.name).split('.')[0]
        file_extension = str(file.name).split('.')[1]
        
        client = OrganizationClient.objects.get(id=client_id)
        uploader = Uploader(request.user, client)
        
        data, stat = uploader.upload_file_to_database(filename=file, file_type=file_extension, table=filename)
        
        if not stat:
            return Response({'error': data}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data)   
             
