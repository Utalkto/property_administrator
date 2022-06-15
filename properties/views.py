# python 
import datetime 

# twilio 
from twilio.rest import Client

# django 

from django.utils import timezone

# rest_framework

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema

# models 
from properties.models import Property, PropertyCountries, PropertyType, Unit, Tenants, Team
from properties.serializers import (PropertiesPostSerializer, CountrySerializer, PropertiesSerializer, 
                                    PropertyTypeSerializer, TeamSerializer, TenantPostSerializer,
                                    TenantSerializer, UnitsSerializerGet, UnitPostSerializer)

from register.models import CustomUser

from logs.models import Log
from logs.serializers import LogSerializer

from candidates.models import Candidate

# modules created for the app
from app_modules.send_email import SendEmail
from app_modules.main import convert_to_bool


# other fucntions
def put_candidate_as_tenant(candidate):
    for adult in candidate.adults_information:
        new_tenant = Tenants(
            landlord=Unit.objects.get(id=candidate.unit.id).properties.landlord,
            unit=Unit.objects.get(id=candidate.unit.id),
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
    property_types = PropertyType.objects.all().order_by('id')
    
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
    responses={200: UnitsSerializerGet()})
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
    unit = Unit.objects.get(id=unit_id)
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
    
    unit = Unit.objects.get(id=candidate.unit.id)
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

class PropertyAPI(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    @swagger_auto_schema(
    responses={200: PropertiesSerializer()})
    def get(self, request,  client_id):
        """ 
        Summary: Get a property a user has or an organization owns 
        
        Args:
            client_id <int> (required) = The id of the client the sets of units are going to be created
            property_id <int><query_parameter> (optional) = The id of the property that is needed, 
            leave empty to get all

        Returns:
            Serializer Class, dictionary, JSON: list of properties that an organization has
        """
        
        if request.GET.get('property_id'):
            properties = Property.objects.filter(id=int(request.GET['property_id']))
            
        else:
            try:
                properties_with_access = request.user.clients_access[f'client-{client_id}']['properties']
            except:
                return Response({
                    'error': 'Invalid access'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            properties = Property.objects.filter(id__in=properties_with_access)
        
        
        serializer = PropertiesSerializer(properties, many=True)
        return Response(serializer.data)
    

    @swagger_auto_schema(
    responses={200: PropertiesPostSerializer()})
    def post(self, request, client_id):
        """ Summary: PropertyAPI POST
        
        paremeters:
            client_id (int)(required): indicates the client to which the property is going to be created 

        Returns:
            JSON: new property object created with provided information
        """
        property_data = request.data.copy()
        
        current_time = timezone.now()
                
        property_data['client'] =  client_id
        property_data['city'] = int(request.data['city'])
        property_data['datetime_created'] = current_time
        property_data['created_by'] = request.user.id
        
        property_serializer = PropertiesPostSerializer(data=property_data)
        
        if property_serializer.is_valid():
            property_serializer.save()
            
            log_data = {
                'client': client_id,
                'made_by': request.user.id,
                'property': property_serializer.data['id'],
                'action': 'CREATE',
                'date_made': current_time,
                'new_data': property_serializer.data                
            }
            
            log_serializer = LogSerializer(data=log_data)
            
            if log_serializer.is_valid():
                log_serializer.save()
            
            
            return Response(property_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': property_serializer.errors,
                }, 
                status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(
    responses={200: PropertiesPostSerializer()})
    def put(self, request, client_id):
        
        """ Summary: PropertyAPI GET

        Returns:
            JSON, dictionary: saying if it was a success
        """            
        try:
            _property:Property = Property.objects.get(int(request.data['property_id']))
        except Property.DoesNotExist:
            return Response(
                {
                    'error': 'Property.DoesNotExist: the property with that id does not exist', 
                }, 
                status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': f'ValueError: property_id must be int'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': f'KeyError: property_id must be provided'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        current_time = timezone.now()
        
        previous_data = PropertiesPostSerializer(_property)
        property_serializer = PropertiesPostSerializer(instance=_property, data=request.data)
        
        if property_serializer.is_valid():
            property_serializer.save()
            
            _property.last_edition_made_by = request.user.id
            _property.last_time_edited = current_time
            _property.save()
            
            log_data = {
                'client': client_id,
                'made_by': request.user.id,
                'property': _property.id,
                'action': 'EDIT',
                'date_made': current_time,
                'previous_data': previous_data,
                'new_data': property_serializer.data                
            }
            
            log_serializer = LogSerializer(data=log_data)
            
            if log_serializer.is_valid():
                log_serializer.save()
            
            return Response(property_serializer.data)
        else:
            return  Response(
                {
                    'error': property_serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, client_id):
        try:
            _property:Property = Property.objects.get(id=int(request.GET['property_id']))
        
        except ValueError:
            return Response({'error': f'ValueError: property_id must be int'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError:
            return Response({'error': f'KeyError: property_id must be provided'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    
        except Property.DoesNotExist:  
            return Response(
                {
                'error': 'Property.DoesNotExist: the property with that id does not exist', 
                }, 
                status=status.HTTP_404_NOT_FOUND)
            
        log_data = {
            'client': client_id,
            'made_by': request.user.id,
            'deleted_property': _property.id,
            'action': 'DELETE',
            'date_made': timezone.now(),
        }
        
        log_serializer = LogSerializer(data=log_data)
        
        if log_serializer.is_valid():
            log_serializer.save()
        
        _property.delete()
        
        return Response(
            {
                'message': 'The property has been deleted'
            })
        
        
class UnitsAPI(APIView):
 
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    @swagger_auto_schema(
    responses={200: UnitsSerializerGet()})
    def get(self, request, client_id):
        
        """ UnitsAPI GET
        
        rent_info <bool><Optional>: indicates if number of units rented and not rented is needed
        
        leases_to_exp <bool><Optional>: indicates if the number of units wich leases are going to exp 
        
        unit_id <int><Optional>: indicates the id of the unit that is needed, if set to "all" 
        returns all the units a client owns
        
        'view_all <bool><Optional>': 'idicates if sent more information when "for_rent" or "lease" are set'
        
        Returns:
            JSON: Unit objects
        """

        if not request.GET:
            return Response({
                'message':'parameters cannot be empty, you must indicate at least one of these parameters:',
                'rent_info (bool)': 'indicates if number of units rented and not rented is needed',
                'leases (bool)': 'indicates if the number of units wich leases are going to exp' ,
                'unit_id (str)': 'indicates the id of the unit that is needed, if set to "all" returns all the units a client owns',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        response = dict()
        view_all = request.GET.get('view_all')
            
        if request.GET.get('rent_info'):
            
            rent_info = Unit.objects.filter(property__client=client_id, rented=False)
            rented = Unit.objects.filter(property__client=client_id, rented=True)

            response['quantity_for_rent'] = rent_info.count()
            response['quantity_rented'] = rented.count()
            
            if view_all:
                response['units_for_rent'] = UnitsSerializerGet(rent_info, many=True).data
                response['units_rented'] = UnitsSerializerGet(rented, many=True).data
                
        delta = datetime.timedelta(days=90)
        
        new_datetime = datetime.datetime.now() + delta
        year = new_datetime.strftime('%Y')
        month = new_datetime.strftime('%m')
        
        if request.GET.get('leases_to_exp'):
            leases_to_exp = Unit.objects.filter(property__client=client_id,
                                          lease_expiration_date__year__lte=year,
                                          lease_expiration_date__month__lte=month)
            
            response['number_of_leases_to_exp'] = leases_to_exp.count()
            if view_all:
                response['units_with_leases_to_exp'] = UnitsSerializerGet(leases_to_exp, many=True).data


        unit_id = request.GET.get('unit_id')
        
        if unit_id is None:
            units = Unit.objects.filter(property__client=client_id)
            units_serializer = UnitsSerializerGet(units, many=True)
        
        else:
            unit_id = int(unit_id)
            try:
                units = Unit.objects.filter(id=unit_id, property__client=client_id)
                units_serializer = UnitsSerializerGet(units, many=True)
                
            except Unit.DoesNotExist:
                return Response(
                    {
                    'error': 'Unit.DoesNotExist: the unit with provided id does not exist', 
                    }, 
                    status=status.HTTP_404_NOT_FOUND)
    
        response['units'] = units_serializer.data
        
        return Response(response)
        
    
    @swagger_auto_schema(
    responses={200: UnitPostSerializer()})
    def post(self, request, client_id):
        
        request.data['client_id'] = client_id
        
        unit_serializer = UnitPostSerializer(data=request.data)
        current_time = timezone.now()
        
        request.data['datetime_created'] = current_time
        request.data['created_by'] = request.user.id
        
        if unit_serializer.is_valid():
            unit_serializer.save()
            
            property:Property = Property.objects.get(id=int(request.data['property']))
            property.number_of_units = property.number_of_units + 1
            property.save()
            
            log_data = {
                'client': client_id,
                'made_by': request.user.id,
                'property': unit_serializer.data['id'],
                'action': 'CREATE',
                'date_made': current_time,
                'new_data': unit_serializer.data                
            }
            
            log_serializer = LogSerializer(data=log_data)
            
            if log_serializer.is_valid():
                log_serializer.save()

            return Response(unit_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': unit_serializer.errors, 
                }, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
    responses={200: UnitPostSerializer()})
    def put(self, request, client_id):
        
        """UnitsAPI PUT
        
        parameters:
            queryparameter:
                unit_id (int)(required): the id of the unit that is going to be modified

        Returns:
            _type_: _description_
        """
        
        try:
            unit = Unit.objects.get(id= request.GET['unit_id'])
        except ValueError:
            return Response({'error': f'ValueError: unit_id must be int'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': f'KeyError: unit_id must be provided'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except Unit.DoesNotExist:
            return Response(
                {
                    'error': 'Unit.DoesNotExist: the unit with provided id does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
        current_time = timezone.now()

        request.data['property_manager'] = request.user.id
        unit_serializer = UnitPostSerializer(instance=unit, data=request.data)
        
        if unit_serializer.is_valid():
            unit_serializer.save()
            
            log_data = {
                'client': client_id,
                'made_by': request.user.id,
                'unit': unit.id,
                'action': 'CREATE',
                'date_made': current_time,
                'new_data': unit_serializer.data                
            }
            
            log_serializer = LogSerializer(data=log_data)
            
            if log_serializer.is_valid():
                log_serializer.save()
            
            return Response(unit_serializer.data)
        else:

            return Response(
                {
                    'error': unit_serializer.errors, 
                }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, client_id):
        unit_id = client_id
        try:
            unit = Unit.objects.get(id=unit_id)
            unit.delete()
            return Response(
                {
                    'message': 'The unit has been eliminated successfully'
                }, 
                status=status.HTTP_200_OK)
        
        except Unit.DoesNotExist:
            return Response(
                {
                    'error': 'Unit.DoesNotExist: the unit with provided id does not exist'
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
                    tenant_property = Property.objects.get(id=t.unit.property.id)
                    unit_number = Unit.objects.get(id=t.unit.id).unit_number
                    
                    data = serializer.data
                    data['property_name'] = tenant_property.name
                    data['property_id'] = tenant_property.id
                    data['unit_number'] = unit_number
                    
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
                    data['property_name'] = Property.objects.get(id=property_id).name
                except Property.DoesNotExist:
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
            serializer =  TenantPostSerializer(data=request.data)
           
            if serializer.is_valid():
                serializer.save()
                
                unit = Unit.objects.get(id=int(request.data['unit']))
                
                if unit.main_tenant_name == 'No tenant':
                    unit.main_tenant_name = request.data['name']
                    unit.save()
                    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            tenant = Tenants.objects.get(id=tenant_id)

            request.data['landlord'] = request.user.id
            serializer = TenantPostSerializer(tenant, data=request.data)
            
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
            team = Team.objects.filter(landlord=request.user.id)
        else:
            try:
                team = Team.objects.filter(id=int(team_id), lanlord=request.user.id)
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
        return Response(serializer.data)
        
        
    def post(self, request):
        
        request.data['landlord'] = request.user.id
        serializer = TeamSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': True, 
                    'message': 'serializer is not valid', 
                    'serializer_error': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, team_id):
        
        team = self.check_if_team_exist(team_id=int(team_id))
            
            
        serializer = TeamSerializer(instance=team, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': True, 
                    'message': 'serializer is not valid', 
                    'serializer_error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, team_id):
        Team.objects.get(id=int(team_id)).delete()

        return Response({'message': 'deleted with success'})
        
            
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