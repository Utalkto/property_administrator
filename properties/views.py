# python 
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import smtplib, ssl

# twilio 
from twilio.rest import Client

# django 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# models 
from properties.models import Properties, Units
from properties.serializers import PropertiesSerializer, TenantSerializer, UnitsSerializer
from register.models import CustomUser


TEST_TOKEN = 'Token 71ed6e07240ac3c48e44b5a43b5c89e453382f2a'

@api_view(['POST'])
def vacantUnit(request, id):

    unit = Units.objects.get(id=id)
    unit.rented = not unit.rented
    unit.save()
    serializer = UnitsSerializer(unit)


    #COMUNICACION POR MENSAJE DE TEXTO
    if unit.rented:
        return Response({"unit": serializer.data})
    else:
        account_sid = "ACe61e701812ddfb138275589f4a556d35"
        auth_token  = "7c25fe7f3dc40bab21cef73caba5065a"

        client = Client(account_sid, auth_token)

        mensaje =   f"{unit.name} entro en proceso de desalojo"
        message = client.messages.create(
            from_="+19035224352", 
            to="+584120148704",
            body= mensaje
        )
        
        #COMUNICACION POR EMAIL
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = 'Move-out Instructions'
        mensaje['From']='hello@orinocoventures.com'
        mensaje['To']='acampos@utalkto.com'
        html = f"""
        <html>
            <body>
                <h1>Eviction instructions</h1>
          
            </body>

        </html>

        """
        parte_html = MIMEText(html,'html')
        mensaje.attach(parte_html)

        # AJUNTANDO ARCHIVO DE DESALOJO
        ajunto = MIMEBase('application', 'octet-stream')
        ajunto.set_payload(open('test.pdf', 'rb').read())
        encoders.encode_base64(ajunto)
        ajunto.add_header('content-Disposition','attachment; filename="test.pdf"')
        mensaje.attach(ajunto)


        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.com", 465, context=context) as server:
            server.login("hello@orinocoventures.com",'Orinoco2022..' )
            server.sendmail(from_addr="hello@orinocoventures.com", to_addrs="acampos@utalkto.com",msg=mensaje.as_string() )


        return Response({"unit": serializer.data})


class PropertiesViewSet(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def get(self, request):
        """ 
        Summary: Get all properties a landord has 
        
        Args:
            request (_type_): data sent from front

        Returns:
            Serializer Class, dictionary, JSON: list of properties that a landlord has
        """
        serializer = PropertiesSerializer(Properties.objects.filter(landlord = request.user.id), many=True)
        return Response(serializer.data)
    

    def post(self, request):
        """
        Summary: create new property 

        Returns:
            JSON: saying if it was a success
        """
    
        request.data['landlord'] = request.user.id
        serializer =  PropertiesSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "property created with success"
                }, 
                status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': True, 
                    'message': 'serializer is not valid', 
                    'serializer_error': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, id):
        
        """
        Summary: update a property

        Returns:
            JSON, dictionary: saying if it was a success
        """
        
        try:
            _property = Properties.objects.get(id=id)
            request.data['landlord'] = request.user.id
            
            _property = PropertiesSerializer(instance=_property, data=request.data)

            if _property.is_valid():
                _property.save()
                Response(
                    {
                        'message': 'the property was updated successfully', 
                        'data': _property.data
                    }, 
                    status=status.HTTP_200_OK)
            else:
                return  Response(
                    {
                        'error': True, 
                        'message': 'serializer is not valid', 
                        'serializer_error': _property.errors
                    }, 
                    status=status.HTTP_400_BAD_REQUEST)

        except Properties.DoesNotExist:
            return Response(
                {
                    'error': True, 
                    'message': 'property does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
    
    
    def delete(self, request, id):
        try:
            _property = Properties.objects.get(id=id)
            _property.delete()
            return Response(
                {
                 "message": "The property has been deleted"
                }, 
                status=status.HTTP_200_OK)
        
        except Properties.DoesNotExist:  
            return Response(
                {'error': True, 
                 'mensaje': 'The property does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
        

# ask about this view
class  UnitsViewSet(APIView):
 
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def get(self,request,id):
        
        try:
            units = Units.objects.filter(properties_id=id , landlord_id=request.user.id)
            serializer = UnitsSerializer(units, many=True)
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK)
            
        except Units.DoesNotExist:
            return Response(
                {'error': True, 
                 'message ': 'unit does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
        
    
    def post(self, request):

        try: 
            request.data['landlord'] = request.user.id
            # !!! 
            propertie = Properties.objects.get(id=request.data['landlord'])
            # here can be an error, this should be in the serializer
            serializer =  UnitsSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                     "message": "the property has been registered Successfully"
                    }, 
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {
                        'error': True, 
                        'message': 'serializer is not valid', 
                        'serializer_error': serializer.errors
                    }, 
                    status=status.HTTP_400_BAD_REQUEST)
       
       # !!! 
        except CustomUser.DoesNotExist:
            return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)

    
    def put(self, request, id):
        
        try:
            unit = Units.objects.get(id=id)

            request.data['landlord'] = request.user.id
            serializer = UnitsSerializer(instance=unit, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(
                    {
                        'error': True, 
                        'message': 'serializer is not valid', 
                        'serializer_error': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST)

        except Units.DoesNotExist:
            return Response(
                {'error': True, 
                 'message': 'the unit does not exist'
                 }, 
                status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id):
        
        try:
            unit = Units.objects.get(id=id)
            unit.delete()
            return Response(
                {
                    "message": "the unit has been eliminated successfully"
                }, 
                status=status.HTTP_200_OK)
        
        except Units.DoesNotExist:
            return Response(
                {'error': True, 
                 'message': 'the unit does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
       
       

class TenantViewSet(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def post(self, request):

        try: 
            request.data['landlord'] = request.user.id
            serializer =  TenantSerializer(data=request.data)
           
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                     'message': 'tenant registered successfully'
                    }, 
                    status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'error': True, 
                     'message': 'serializer is not valid', 
                     'serializer_error': serializer.errors
                    }, 
                    status=status.HTTP_400_BAD_REQUEST)
        
        #!!! why is this here?
        except CustomUser.DoesNotExist:
            return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)
        
    
    # should here be a view to get the tenants who live in a unit/property?
      


        