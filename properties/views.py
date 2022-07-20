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
from .models import Property, PropertyCountries, PropertyType, Unit, Tenants, Team
from .serializers import (PropertyRelatedFieldsSerializer, CountrySerializer, PropertySerializer, 
                                    PropertyTypeSerializer, TeamSerializer, TenantRelatedFieldsSerializer,
                                    TenantSerializer, UnitSerializer, UnitRelatedFieldsSerializer)

from register.models import CustomUser, Organization
from register.serializers import UserSerializer

from logs.extra_modules import register_log

from candidates.models import Candidate

# modules created for the app
from app_modules.send_email import SendEmail
from app_modules.permission import user_has_access

from .queryserializer import PropertyAPIQuerySerializer, TenantAPIQuerySerializer, UnitAPIQueryserializer
from drf_yasg import openapi
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

# API --------------------------------------------
# ------------------------------------------------

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
    responses={200: UnitRelatedFieldsSerializer()})
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def vacantUnit(request, unit_id):
    
    """Unidad (vacante/alquilada)

    Establece la desocupación de una unidad de, alquilada a libre y envia un mensaje al arrendador notificando
    él cambio y las instrucciones para mudarse a los inquilinos
        
    Argumentos :
        unit_id int: unidad unit_id

    Devoluciones :
        Clase de serializador, diccionario, JSON: lista de propiedades que un propietario tiene # cambie aquí    
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
    query_serializer= PropertyAPIQuerySerializer(),
    responses={200: PropertyRelatedFieldsSerializer()})
    def get(self, request,  client_id):
        """Obtiene propiedad(es)

        Descripcion : lista todas las propiedades que pertenecen a un usuario.

        Argumentos :
            client_id (int) (obligatorio) = El id del cliente se van a crear los conjuntos de unidades
            property_id (int)(query_parameter) (opcional) = El id de la propiedad que se necesita,
            dejar vacío para obtener todo.

        Devoluciones :
            Clase de serializador, diccionario, JSON: lista de propiedades que tiene una organización.
        """
        
        if request.GET.get('property_id'):
            properties = Property.objects.filter(id=int(request.GET['property_id']))
            
        else:
            if client_id == 'all':
                properties_with_access = list()
                for key in request.user.clients_access.keys():
                    access = request.user.clients_access[key]['properties']
                    properties_with_access.extend(access)
            else:
                try:
                    client_id = int(client_id)
                    properties_with_access = request.user.clients_access[client_id]['properties']
                except ValueError:
                    return Response({
                        'error': 'ValueError: the value of client_id is not valid it must be int or set to "all"'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                except:
                    return Response({
                        'error': 'Invalid access'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            
            properties = Property.objects.filter(id__in=properties_with_access)
        
        
        serializer = PropertyRelatedFieldsSerializer(properties, many=True)
        return Response(serializer.data)
    

    @swagger_auto_schema(
    request_body=PropertySerializer(),
    responses={200: PropertySerializer()})
    def post(self, request, client_id):
        """Crea Propiedad

        Crea la propiedad a un cliente determinado.

        parámetros:
            client_id (int)(obligatorio): indica el cliente al que se le va a crear la propiedad

        Devoluciones:
            JSON: nuevo objeto de propiedad creado con la información proporcionada
        """
        property_data = request.data.copy()
        
        current_time = timezone.now()
                
        property_data['client'] =  client_id
        property_data['city'] = int(request.data['city'])
        property_data['datetime_created'] = current_time
        property_data['created_by'] = request.user.id
        
        property_serializer = PropertySerializer(data=property_data)
        
        if property_serializer.is_valid():
            property_serializer.save()
            request.user.clients_access[int(client_id)]['properties'].append(property_serializer.data['id'])
            request.user.save()
            
            register_log(made_by=request.user.id, 
                        action=1, 
                        client_id=client_id, 
                        date_made=current_time, 
                        property_id=property_serializer.data['id'], 
                        new_data=property_serializer.data)
            
            return Response(property_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': property_serializer.errors,
                }, 
                status=status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        "property_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "address": openapi.Schema(type=openapi.TYPE_STRING),
        #"coordinates":openapi.Schema(type=openapi.TYPE_OBJECT),
        "maps_url": openapi.Schema(type=openapi.TYPE_STRING),
        "name": openapi.Schema(type=openapi.TYPE_STRING),
        "number_of_units": openapi.Schema(type=openapi.TYPE_INTEGER),
        "price_paid": openapi.Schema(type=openapi.TYPE_INTEGER),
        #"photos": openapi.Schema(type=openapi.TYPE_OBJECT),
        "year_built": openapi.Schema(type=openapi.TYPE_INTEGER),
        "year_bought": openapi.Schema(type=openapi.TYPE_INTEGER),
        #"datetime_created": "2022-07-01T20:29:18.524Z",
        #"last_time_edited": "2022-07-01T20:29:18.524Z",
        "client": openapi.Schema(type=openapi.TYPE_INTEGER),
        "city": openapi.Schema(type=openapi.TYPE_INTEGER),
        "property_type": openapi.Schema(type=openapi.TYPE_INTEGER),
    }),

    responses={200: PropertySerializer()})
    def put(self, request, client_id):
        
        """ actualiza Propiedad

        parámetros:
            client_id (int)(obligatorio): indica el cliente al que se le va a actualizar la propiedad
            property_id (int): indica la propiedad a acutualizar.

        Devoluciones:
            JSON, diccionario: informando si fue un éxito.
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
        
        previous_data = PropertySerializer(_property)
        property_serializer = PropertySerializer(instance=_property, data=request.data)
        
        if property_serializer.is_valid():
            property_serializer.save()
            
            _property.last_edition_made_by = request.user.id
            _property.last_time_edited = current_time
            _property.save()
            
            register_log(made_by=request.user.id, 
                    action=2, 
                    client_id=client_id, 
                    date_made=current_time, 
                    property_id=property_serializer.data['id'], 
                    previous_data=previous_data,
                    new_data=property_serializer.data)
            
            return Response(property_serializer.data)
        else:
            return  Response(
                {
                    'error': property_serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST)
  
  
    @swagger_auto_schema(
    query_serializer= PropertyAPIQuerySerializer(),
    responses={200: PropertySerializer()})  
    def delete(self, request, client_id):
        """Elimina Propiedad

        Elimina propiedad

        parámetros:
            client_id (int)(obligatorio): indica el cliente al que se le va a eliminar la propiedad
            property_id (int): indica la propiedad a eliminar.

        Devoluciones:
            Mansaje: informando si fue un éxito.
        """
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
        
        register_log(made_by=request.user.id, 
                    action=3, 
                    client_id=client_id, 
                    date_made=timezone.now(), 
                    property_id=_property.id)
        
        _property.delete()
        
        return Response(
            {
                'message': 'The property has been deleted'
            })
        
        
class UnitsAPI(APIView):
 
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    @swagger_auto_schema(
    responses={200: UnitRelatedFieldsSerializer()})
    def get(self, request, client_id):
        """Obtener Unidad(es)
        
        rent_info (bool)(Optional) here : indicates if number of units rented and not rented is needed
        
        leases_to_exp (bool)(Optional) : indicates if the number of units which leases are going to exp 
        
        unit_id (int)(Optional) : indicates the id of the unit that is needed, if set to "all" 
        returns all the units a client owns
        
        get_general_info (bool)(Optional) : indicates to get the general infomation of units objects, when this is 
        set, unit_id must be givem too 
        
        'view_all (bool)(Optional)' : 'idicates if send more information when "for_rent" or "lease" are set'
        
        Returns :
            JSON : Unit objects
        """

        if not request.GET:
            return Response({
                'message':'parameters cannot be empty, you must indicate at least one of these parameters:',
                'rent_info (bool)': 'returns the number of units that are rented and not rented',
                'leases (bool)': 'returns the number of units wich leases are going to exp' ,
                'unit_id (str)': 'returns the info of the id given, if set to "all" returns all the units a client owns',
                'get_general_info (bool)(Optional)': 'indicates to get the general infomation of units objects, when this is set, unit_id must be givem too',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        response = dict()
        view_all = request.GET.get('view_all')
        unit_id = request.GET.get('unit_id')
        units_serializer:UnitRelatedFieldsSerializer = None
        
        if client_id != 'all':
            try:
                client_id = int(client_id)
            except:
                return Response(
                    {
                        'ValueError:': 'invalid client_id, este debe ser un int o set to all'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            if not user_has_access(request.user, client_id=client_id):
                    return Response(
                        {
                            'error': 'User has not access to this client'
                        }, status=status.HTTP_401_UNAUTHORIZED)
            
            property_list = request.user.clients_access[client_id]['properties']
        
        else:
            property_list = list()            
            for key in request.user.clients_access.keys():
                property_list += request.user.clients_access[key]['properties']
        
            
        if request.GET.get('rent_info'):
            
            if client_id == 'all':
                
                list_of_clients = request.user.clients_access.keys()
                
                for_rent = Unit.objects.filter(property__client__in=list_of_clients, property__in=property_list, rented=False)
                rented = Unit.objects.filter(property__client__in=list_of_clients, property__in=property_list, rented=True)
                
            else:
                try:
                    client_id = int(client_id)
                except ValueError:
                    return Response({'error': 'ValueError: client id must be int'})
                
                # validate the client id to see if it can be accessed to the user
                
                if int(client_id) in request.user.clients_access.keys():
                    for_rent = Unit.objects.filter(property__client=client_id, property__in=property_list, rented=False)
                    rented = Unit.objects.filter(property__client=client_id, property__in=property_list, rented=True)
                else:
                    return Response({
                        'error': 'Access is not valid'
                    }, status=status.HTTP_401_UNAUTHORIZED)

            response['quantity_for_rent'] = for_rent.count()
            response['quantity_rented'] = rented.count()
            
            if view_all:
                response['units_for_rent'] = UnitRelatedFieldsSerializer(for_rent, many=True).data
                response['units_rented'] = UnitRelatedFieldsSerializer(rented, many=True).data
                
        delta = datetime.timedelta(days=90)
        
        new_datetime = datetime.datetime.now() + delta
        year = new_datetime.strftime('%Y')
        month = new_datetime.strftime('%m')
        
        if request.GET.get('leases_to_exp'):
            leases_to_exp = Unit.objects.filter(property__client=client_id,
                                        property__in=property_list,
                                        lease_expiration_date__year__lte=year,
                                        lease_expiration_date__month__lte=month)
            
            response['number_of_leases_to_exp'] = leases_to_exp.count()
            if view_all:
                response['units_with_leases_to_exp'] = UnitRelatedFieldsSerializer(leases_to_exp, many=True).data


        if request.GET.get('get_general_info'):
            
            if unit_id is None:
                return Response({
                    'error': 'KeyError : when get_general_info is set, unit_id must be given (set to "all" to return all the units a client owns)',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            if unit_id == 'all':
                if client_id == 'all':
                    client_list = request.user.clients_access.keys()
                    units = Unit.objects.filter(property__client__in=client_list)
                    
                else:
                    client_id = int(client_id)
                    units = Unit.objects.filter(property__client=client_id, property__in=property_list)
                    
                units_serializer = UnitRelatedFieldsSerializer(units, many=True)
            
            else:
                unit_id = int(unit_id)
                try:
                    units = Unit.objects.filter(id=unit_id, property__client=client_id)
                    units_serializer = UnitRelatedFieldsSerializer(units, many=True)
                    
                except Unit.DoesNotExist:
                    return Response(
                        {
                        'error': 'Unit.DoesNotExist: the unit with provided id does not exist', 
                        }, 
                        status=status.HTTP_404_NOT_FOUND)
        
        
        if units_serializer:
            response['units'] = units_serializer.data
        
        return Response(response)
        
    
    @swagger_auto_schema(
    request_body=UnitSerializer(),
    responses={200: UnitSerializer()})
    def post(self, request, client_id):
        """Crear Unidad

        Descripcion : 

        
        """
        
        request.data['client_id'] = client_id
        
        unit_serializer = UnitSerializer(data=request.data)
        current_time = timezone.now()
        
        request.data['datetime_created'] = current_time
        request.data['created_by'] = request.user.id
        
        if unit_serializer.is_valid():
            unit_serializer.save()
            
            property:Property = Property.objects.get(id=int(request.data['property']))
            property.number_of_units = property.number_of_units + 1
            property.save()
            
            register_log(made_by=request.user.id, 
                action=1, 
                client_id=client_id, 
                date_made=current_time, 
                unit_id=unit_serializer.data['id'], 
                new_data=unit_serializer.data)

            return Response(unit_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': unit_serializer.errors, 
                }, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
    responses={200: UnitSerializer()})
    def put(self, request, client_id):
        """Modifica Unidad
        
        Parametros :
            client_id (int) : id del cliente el cual pertenece esa unidad.
            unit_id (int)(obligatorio): el id de la unidad que se va a modificar.
        """
        
        try:
            unit:Unit = Unit.objects.get(id=request.GET['unit_id'])
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

        request.data['last_time_edited'] = current_time
        request.data['last_edition_made_by'] = request.user.id
        previous_data = UnitSerializer(unit)
        
        unit_serializer = UnitSerializer(instance=unit, data=request.data)
        
        if unit_serializer.is_valid():
            
            register_log(made_by=request.user.id, 
                action=2, 
                client_id=client_id, 
                date_made=current_time, 
                unit_id=unit_serializer.data['id'], 
                previous_data=previous_data,
                new_data=unit_serializer.data)           

            unit_serializer.save()
            unit.last_edition_made_by = request.user.id
            unit.last_time_edited = current_time
            unit.save()
            
            return Response(unit_serializer.data)
        else:

            return Response(
                {
                    'error': unit_serializer.errors, 
                }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
    query_serializer=UnitAPIQueryserializer(),
    responses={200: "correct"})
    def delete(self, request, client_id):
        """Elininar Unidad

        Argumentos :

            client_id (int) (obligatorio) = El id del cliente asocioado a esa unidad.
            property_id (int)(query_parameter) (opcional) = El id de la propiedad a eliminar.
        
        """
        
        try:
            unit:Unit = Unit.objects.get(id= request.GET['unit_id'])
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
        
        register_log(made_by=request.user.id, 
                action=3, 
                client_id=client_id, 
                date_made=timezone.now(), 
                unit_id=unit.id)  
        
        unit.delete()
        
        return Response(
            {
                'message': 'The unit has been eliminated successfully'
            })
     

class TenantViewSet(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
 
    @swagger_auto_schema(
    query_serializer= TenantAPIQuerySerializer(),
    responses={200: TenantRelatedFieldsSerializer()})
    def get(self, request, client_id):
        """Obtener cliente(s)

        Deccripcion : Devuelve los inqulinos asociados a ese usuario

        Argumentos :
            client_id (str) (requerido): devuelve los inquilinos asociados con ese cliente
            inquilino (int) (opcional): devuelve los datos asociados a esa identificación de inquilino
        """
        
        if client_id == 'all':
            clients_with_access = request.user.clients_access.keys()
            tenants = Tenants.objects.filter(unit__property__client__in=clients_with_access, deleted=False)
        
        else:
            try: 
                client_id = int(client_id)
                tenant_id = request.GET['tenant_id']
                
                if client_id not in request.user.clients_access.keys():
                    return Response({'error': 'Access is not valid'}, status=status.HTTP_401_UNAUTHORIZED)
                    
                
            except ValueError:
                    return Response({
                        'error': 'ValueError: the value of client_id is not valid it must be int or set to "all"'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                 return Response({
                        'error': 'KeyError: tenant_id was not supplied, set to "all" to get all tenants'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            if tenant_id == 'all':
                tenants = Tenants.objects.filter(unit__property__client=client_id, deleted=False)
            else:
                try:
                    tenant_id = int(tenant_id)
                except ValueError:
                    return Response({
                            'error': 'ValueError: the value of tenant_id is not valid it must be int or set to "all" to get all tenants'
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                tenants = Tenants.objects.filter(id=tenant_id, deleted=False)
                
                if not len(tenants):
                    return Response({'error': 'Tenant.DoesNotExist: tenant with that id does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        tenants_serializer = TenantRelatedFieldsSerializer(tenants, many=True)
        return Response(tenants_serializer.data)
    
    
    @swagger_auto_schema(
    request_body=TenantSerializer(),
    responses={200: TenantRelatedFieldsSerializer()})
    def post(self, request, client_id):
        
        """Crear Inqulinos
        
        Argumentos : 
            client_id (int)(obligatorio): el cliente con el que se asociará el arrendatario
            unidad (int)(obligatorio): la unidad con la que se asociará el inquilino

        """

        current_time = timezone.now()
        
        request.data['datetime_created'] = current_time
        request.data['created_by'] = request.user.id

        tenant_serializer = TenantSerializer(data=request.data)
        
        if tenant_serializer.is_valid():
            tenant_serializer.save()
            
            unit:Unit = Unit.objects.get(id=int(request.data['unit']))
            
            if unit.main_tenant_name == 'No tenant':
                unit.main_tenant_name = request.data['name']
                unit.save()
                
            register_log(
                made_by=request.user.id,
                action=1,
                client_id=client_id,
                date_made=current_time,
                new_data=tenant_serializer.data
            )
                
            return Response(tenant_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': tenant_serializer.errors, 
                }, status=status.HTTP_400_BAD_REQUEST)
        
    
    @swagger_auto_schema(
    responses={200: TenantRelatedFieldsSerializer()})
    def put(self, request, client_id):
        
        """Actualiza inquilinos
        
        Argumentos :
            client_id (int)(obligatorio): el cliente con el que se asociará el arrendatario
            tent_id (int)(obligatorio): el inquilino que se modificará
        """
        
        key_valid, response = self.validate_key(key_name='tenant_id', get_dict=request.GET)
        
        if not key_valid:
            return Response(response[0]['message'], status=response[0]['status'])
        else:
            tenant = response

        current_time = timezone.now()
        
        request.data['last_time_edited'] = current_time
        request.data['last_edition_made_by'] = request.user.id
        
        previous_data = TenantSerializer(tenant)
        tenant_serializer = TenantSerializer(tenant, data=request.data)
        
        if tenant_serializer.is_valid():
            tenant_serializer.save()
            
            register_log(made_by=request.user.id,
                        action=2,
                        client_id=client_id,
                        date_made=current_time,
                        previous_data=previous_data,
                        new_data=tenant_serializer.data)
            
            return Response(tenant_serializer.data)
        else:
            return Response(
                {
                    'error': tenant_serializer.errors, 
                }, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
    query_serializer= TenantAPIQuerySerializer(),
    responses={200: TenantRelatedFieldsSerializer()})    
    def delete(self, request, client_id):
        
        """Elimina Inqulinos
        
        Argumentos :
            client_id (int)(obligatorio): el cliente con el que esta asociado el arrendatario
            tent_id (int) (obligatorio): el inquilino que se eliminará
        """

        key_valid, response = self.validate_key(key_name='tenant_id', get_dict=request.GET)
        
        if not key_valid:
            return Response(response[0]['message'], status=response[0]['status'])
        else:
            tenant:Tenants = response
            

        register_log(
            made_by=request.user.id,
            action=3,
            client_id=client_id,
            date_made=timezone.now(),
        )
            
        tenant.deleted = True
        tenant.save()
        return Response(
            {
                "message": "the tenant has been eliminated successfully"
            })
        
        
    # -----------------------------------------------------------
    # OTHER FUNCTIONS -------------------------------------------
        
    def validate_key(slef, key_name:str, get_dict:dict) -> bool:
        
        try:
            tenant = Tenants.objects.get(id=int(get_dict[key_name]))
        
        except KeyError:
            response = { 
                       'message':{
                            'error': f'KeyError: {key_name} must be provided as int'
                            },
                        'status':status.HTTP_400_BAD_REQUEST
                       },
            
            return False, response
        
        except ValueError:
            response = { 
                       'message':{
                            'error': f'ValueError: {key_name} must be int',
                            },
                        'status':status.HTTP_400_BAD_REQUEST
                       },
            
            return False, response
        
        except Tenants.DoesNotExist:
            
            response = { 
                       'message':{
                            'error': 'Tenants.DoesNotExist: the tenant with provided id does not exist',
                            },
                        'status':status.HTTP_404_NOT_FOUND
                       },
            
            return False, response

        return True, tenant


class TeamApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,) 
    
    def get(self, request, organization_id):
        
        """Retorna los usuarios que posee una organization
        
        query parameters:
            client_id (int): el id del cliente que de los que se quiere obtener, dejarlo en blanco para obtener todas

        Returns:
            _type_: _description_
        """
        
        if not user_has_access(user=request.user, organization_id=organization_id):
            return Response({'error': 'Access is not valid'})
        
        
        if request.GET.get('client_id') is None:
            
            try: organization = Organization.objects.get(id=organization_id)
            except Organization.DoesNotExist:
                return Response({'error': 'Organization.DoesNotExist'})
            
            team = organization.customuser_set.all()
            users_serializer = UserSerializer(team, many=True)

        else:
            try: 
                client_id = int(request.GET.get('client_id'))
            
                team = CustomUser.objects.filter(organization=organization_id)
                part_of_team = list()
                
                for user in team:
                    
                    if client_id in user.clients_access.keys():
                        part_of_team.append(user)
                
                users_serializer = UserSerializer(part_of_team, many=True)
            
            except ValueError:
                return Response({'error': 'ValueError: client_id debe ser int'})
            
        
        return Response(users_serializer.data)


# ALL THESE PARTS MUST BE DEPRECATED

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