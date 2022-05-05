# python 
# twilio 
from twilio.rest import Client

# django 
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from django.db.models import Q

# models 
from properties.models import Properties, Units, Tenants
from properties.serializers import PropertiesSerializer, TenantSerializer, UnitsSerializer
from register.models import CustomUser

# modules created for the app

from app_modules.send_email import SendEmail

TEST_TOKEN = 'Token 71ed6e07240ac3c48e44b5a43b5c89e453382f2a'

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def vacantUnit(request, id):
    
    """ 
        Summary: Set the vacant of a unit from rented to free and send a message to the landlord notifiying
        him and the instructions for moving out to the tenants
        
        Args:
            id (_type_): IntegerField

        Returns:
            Serializer Class, dictionary, JSON: list of properties that a landlord has
            
        """
    unit = Units.objects.get(id=id)
    unit.rented = not unit.rented
    unit.save()
    serializer = UnitsSerializer(unit)
    
    tenants_in_unit = Tenants.objects.filter(Q(unit=unit.id))
    landlord = CustomUser.objects.get(id=unit.landlord.id)
    
    # Twilio settings 
    # this must change to the app twilio account
    account_sid = "AC169f0dd1f79d9a78e183de54363307bb" 
    auth_token  = "15c699a3cf3f29fcc776a47259e58593"

    # twilio client
    client = Client(account_sid, auth_token)
    
    twilio_message =  f"The proccess for moving out has started in the next unit:, {unit.name}"
    twilio_message = client.messages.create(
        from_="+19704897499", 
        to=landlord.phone,
        body= twilio_message
    )
    

    # email settings

    for tenant in tenants_in_unit:
        
        SendEmail(
        send_to= tenant.email,
        subject= f'Move-out Instructions',
        html = f"""
                <html>
                    <body>
                        <h1>Eviction instructions</h1>
                    </body>
                </html>
                """,
        attach_file = 'test.pdf'
        )
    

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
        serializer = PropertiesSerializer(data=request.data)
        
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
                {
                'error': True, 
                 'message ': 'unit does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
        
    
    def post(self, request):

        try: 
            request.data['landlord'] = request.user.id
            
            # !!! 
            _property = Properties.objects.get(id=request.data['landlord'])
            # here can be an error, this should be in the serializer?
            
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
                    {
                    'error': True, 
                     'message': 'serializer is not valid', 
                     'serializer_error': serializer.errors
                    }, 
                    status=status.HTTP_400_BAD_REQUEST)
        
        #!!! why is this here?
        except CustomUser.DoesNotExist:
            return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)
        
      


        