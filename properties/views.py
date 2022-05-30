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

from drf_yasg.utils import swagger_auto_schema


# models 
from properties.models import Properties, PropertyCities, PropertyCountries, PropertyTypes, Units, Tenants, Team
from properties.serializers import PropertiesPostSerializer, CountrySerializer, PropertiesSerializer, PropertyTypeSerializer, TeamSerializer, TenantSerializer, UnitsSerializer, UnitsSerializerNoTenant, UnitSerializerPost

from register.models import CustomUser

from candidates.models import Candidate

# modules created for the app
from app_modules.send_email import SendEmail



TEST_TOKEN = 'Token 71ed6e07240ac3c48e44b5a43b5c89e453382f2a'


# other fucntions

def put_candidate_as_tenant(candidate):
    
    for adult in candidate.adults_information:
        new_tenant = Tenants(
            landlord=Units.objects.get(id=candidate.unit.id).properties.landlord,
            unit=Units.objects.get(id=candidate.unit.id),
            email=candidate.adults_information[adult]['email'],
            name=candidate.adults_information[adult]['name']
            )
        
        new_tenant.save()
    return "created"


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def data_to_create_property(request):
    
    countries = PropertyCountries.objects.all()
    property_types = PropertyTypes.objects.all()
    
    countries_serializer = CountrySerializer(countries, many=True)
    property_type_serializer = PropertyTypeSerializer(property_types, many=True)
    
    return Response(
        {
            'data': {
                'countries': countries_serializer.data,
                'property_types': property_type_serializer.data
            }
        })
    
# ---------------------------------------------------
# post 

@swagger_auto_schema(
    method='post',
    responses={200: UnitsSerializer()})
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def vacantUnit(request, unit_id):
    
    """ 
        Summary: Set the vacant of a unit from rented to free and send a message to the landlord notifiying
        him and the instructions for moving out to the tenants
        
        Args:
            unit_id int: unit unit_id

        Returns:
            Serializer Class, dictionary, JSON: list of properties that a landlord has # change here 
            
        """
    unit = Units.objects.get(id=unit_id)
    unit.rented = not unit.rented
    unit.save()
    
    tenants_in_unit = Tenants.objects.filter(Q(unit=unit.id))
    landlord = CustomUser.objects.get(id=unit.properties.landlord.id) # There is a typo here
    
    # Twilio settings 
    # this must change to the app twilio account
    account_sid = "AC169f0dd1f79d9a78e183de54363307bb" 
    auth_token  = "15c699a3cf3f29fcc776a47259e58593"

    # twilio client
    client = Client(account_sid, auth_token)
    
    twilio_message =  f"The proccess for moving out has started in the next unit:s {unit.name}"
    twilio_message = client.messages.create(
        from_="+19704897499", 
        to=landlord.phone,
        body= twilio_message
    )


    # email settings
    emails_sent_to:dict = {}
    
    for index, tenant in enumerate(tenants_in_unit):
        
        emails_sent_to[f'tenat{index}'] = [tenant.email]
        
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
    

    return Response({"unit": 'status changed successfully', 'emails_sent_to': emails_sent_to})


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def set_unit_rented(request, candidate_id):
    
    """
    Documentation here
    """
    
    candidate = Candidate.objects.get(id=candidate_id)
    candidate.status = 3
    candidate.save()
    
    unit = Units.objects.get(id=candidate.unit.id)
    unit.rented = True
    
    unit.number_of_residents = candidate.number_of_children + candidate.number_of_adults
    unit.number_of_pets = candidate.pets[0]
    unit.pets_living = candidate.pets[1:]
    
    extra_residents = unit.rooms * 2 - len(candidate.adults_information.keys())
    
    if extra_residents < 0:
        unit.extra_resident = abs(extra_residents)
    else:
        unit.extra_resident = 0
    unit.save()
    
    
    put_candidate_as_tenant(candidate) 
    
    
    # TODO: put the unit out of market (facebook marketplace and kijiji)
    
    emails_sent_to: dict = {}
    
    
    for index, adult in enumerate(candidate.adults_information):
        
        emails_sent_to[f'adult{index}'] = candidate.adults_information[adult]['email']

        SendEmail(
            send_to= candidate.adults_information[adult]['email'],
            subject= 'Move in instructions',
            html= f"""
                    <html>
                        <body>
                            <h1>Dear {candidate.adults_information[adult]['name']}, here are attached the move in information</h1>
                        </body>
                    </html>
                    """,
            attach_file='test.pdf'
            )
    
    return Response(
        {
            'message': 'email(s) sent successfully',
            'sent_to': emails_sent_to
        }, status=status.HTTP_200_OK)


# CLASSES --------------------------------------

class PropertiesViewSet(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    @swagger_auto_schema(
    responses={200: PropertiesSerializer()})
    def get(self, request, property_id):
        """ 
        Summary: Get all properties a landord has 
        
        Args:
            request (_type_): data sent from front

        Returns:
            Serializer Class, dictionary, JSON: list of properties that a landlord has
        """
        
        if property_id == 0:
            serializer = PropertiesSerializer(Properties.objects.filter(landlord = request.user.id), many=True)
            # city name 
            # property type string
            
        else:
            serializer = PropertiesSerializer(Properties.objects.filter(landlord = request.user.id, id = property_id), many=True)
        
        return Response(serializer.data)
    

    @swagger_auto_schema(
    responses={200: PropertiesPostSerializer()})
    def post(self, request):
        """
        Summary: create new property 

        Returns:
            JSON: saying if it was a success
        """
        data = request.data.copy()
        
        data['landlord'] =  request.user.id
        
        
        serializer = PropertiesPostSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "property created with success",
                    'property': serializer.data
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
    
    
    @swagger_auto_schema(
    responses={200: PropertiesPostSerializer()})
    def put(self, request, property_id):
        
        """
        Summary: update a property

        Returns:
            JSON, dictionary: saying if it was a success
        """
        
        try:
            _property = Properties.objects.get(id=property_id)
            request.data['landlord'] = request.user.id
            
            _property = PropertiesPostSerializer(instance=_property, data=request.data)

            if _property.is_valid():
                _property.save()
                return Response(
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
    
    
    def delete(self, request, property_id):
        try:
            _property = Properties.objects.get(id=property_id)
            _property.delete()
            return Response(
                {
                'message': 'The property has been deleted'
                }, 
                status=status.HTTP_200_OK)
        
        except Properties.DoesNotExist:  
            return Response(
                {
                'error': True, 
                'mensaje': 'The property does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
    

class UnitsViewSet(APIView):
 
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    @swagger_auto_schema(
    responses={200: UnitsSerializer()})
    def get(self, request, unit_id):
         
        if unit_id == 0:
            
            units = Units.objects.filter(property_manager=request.user.id)
            
            serializer = UnitsSerializer(units, many=True)
            
            return Response(
                serializer.data, 
                status=status.HTTP_200_OK)
        
        try:
            units = Units.objects.filter(id=unit_id , property_manager=request.user.id)
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
        
    
    @swagger_auto_schema(
    responses={200: UnitSerializerPost()})
    def post(self, request, unit_id):

        try: 
            request.data['landlord'] = request.user.id
            
            _property = Properties.objects.get(id=request.data['landlord'])
            
            serializer =  UnitSerializerPost(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, 
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

    
    @swagger_auto_schema(
    responses={200: UnitsSerializer()})
    def put(self, request, unit_id):
        
        try:
            unit = Units.objects.get(id=unit_id)

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


    def delete(self, request, unit_id):
        
        try:
            unit = Units.objects.get(id=unit_id)
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
 

    def get(self, request, tenant_id, property_id):
        
        # to get all tenants send tenant_id == 0
        
        data_to_return = list()
        
        if tenant_id == 0:
            
            if property_id == 0:
                
                tenants = Tenants.objects.filter(
                        unit__property_manager__id = request.user.id)
                
                for t in tenants:
                    
                    serializer = TenantSerializer(t)
                    tenant_property =  Properties.objects.get(id=t.unit.property.id)
                    
                    data = serializer.data
                    data['property_name'] = tenant_property.name
                    data['property_id'] = tenant_property.id
                    
                    data_to_return.append(data)

            # get all tenants in a unit 
            else:
                serializer = TenantSerializer(
                    Tenants.objects.filter(
                        unit__property_manager__id = request.user.id, 
                        unit__property__id = property_id), 
                    many=True)
                
                data = dict()
                
                data['tenants'] = serializer.data
                
                try :
                    data['property_name'] = Properties.objects.get(id=property_id).name
                except Properties.DoesNotExist:
                    return Response(
                        {
                            'error': True,
                            'message': 'Property does not exist'
                        }, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                data_to_return = data
           
            return Response(data_to_return, status=status.HTTP_200_OK)

  
        serializer = TenantSerializer(Tenants.objects.filter(id=tenant_id, unit__property_manager__id = request.user.id), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
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
        
      
        except CustomUser.DoesNotExist:
            return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)


    def put(self, request, tenant_id, property_id):

        try:
            unit = Tenants.objects.get(id=tenant_id)

            request.data['landlord'] = request.user.id
            serializer = TenantSerializer(instance=unit, data=request.data)
            
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

        except Tenants.DoesNotExist:
            return Response(
                {'error': True, 
                 'message': 'the unit does not exist'
                 }, 
                status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, tenant_id, property_id):

        try:
            tenent = Tenants.objects.get(id=tenant_id)
            tenent.delete()
            return Response(
                {
                    "message": "the tenent has been eliminated successfully"
                }, 
                status=status.HTTP_200_OK)
        
        except Tenants.DoesNotExist:
            return Response(
                {'error': True, 
                 'message': 'the tenent does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)  


class TeamApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def get(self, request, team_id):
        
        if team_id == 'all':
            team = Team.objects.all()
        else:
            try:
                team = Team.objects.filter(id=int(team_id))
            except Team.DoesNotExist:
                return Response(
                        {
                            'error': True,
                            'message': 'team object with that id does not exist'
                        }, status=status.HTTP_404_NOT_FOUND
                    )
            except:
                return Response(
                        {
                            'error': True,
                            'message': 'id provided is not valid'
                        }, status=status.HTTP_400_BAD_REQUEST
                    )
            
        serializer = TeamSerializer(team, many=True)
        return Response(serializer)
        
        
    def post(self, request):
        
        serializer = TeamSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                    {
                     'message': 'created'
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
    
    
    def put(self, request, team_id):
        
        team = self.check_if_team_exist(team_id=team_id)
            
            
        serializer = TeamSerializer(instance=team, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                    {
                     'message': 'created'
                    }, 
                    status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': True, 
                    'message': 'serializer is not valid', 
                    'serializer_error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, team_id):
        team = self.check_if_team_exist(team_id=team_id)
        team.delete()
        
            
    def check_if_team_exist(self, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                    {
                        'error': True,
                        'message': 'team object with that id does not exist'
                    }, status=status.HTTP_404_NOT_FOUND
                )
            
        return team
    