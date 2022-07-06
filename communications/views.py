# python
# django 

from django.shortcuts import render
from django.http import HttpResponse

# rest_framework

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.utils import timezone

# twilio 
from twilio.rest import Client

from communications.models import Conversation, Message
from register.models import Organization

# serializers

from .serializers import ConversationRelatedFieldsSerializer, ConversationSerializer, MessageSerializer
from .models import Message
from django.utils import timezone

# property modules

from properties.models import Tenants, Team
from tickets.models import Suppliers

# same app modules 
from app_modules.send_email import SendEmail
from app_modules.decorators import check_login
from app_modules.main import convert_to_bool

from .extra_modules import save_message_in_database, check_status_of_twilio_call
from app_modules.permission import user_has_access

from drf_yasg.utils import swagger_auto_schema
import datetime

from jobs.updater import SCHEDULER

ACCOUNT_SID = 'AC07f9df720f406836bf36885a0795dd66'
TWILIO_AUTH_TOKEN = 'c5dbc722f8f448bbbfd5197fada23bc5'


def filter_messages_by_via(filter_by:str) -> list:
    
    VIAS = ['EMAIL', 'SMS', 'CALL']
    list_to_filter = list()
    
    
    if filter_by is not None:
        
        filter_by = filter_by.split(',')
       
        for filter_str in filter_by:
            if filter_str not in VIAS:
                return Response({'error': 'ValueError: filter_by debe ser EMAIL, SMS, por defecto ya is set to "all"'},
                                status=status.HTTP_400_BAD_REQUEST)
        
        list_to_filter.append(filter_str)
    
    elif filter_by is None:
        list_to_filter = VIAS.copy()
        
    return list_to_filter



# API -----------------------------------------------


class ConversationsAPI(APIView):
    
    """
    
    class to manage all the communications the app needs to do with tenants
    
    """
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    def get(self, request, client_id:int):
        
        """Obtener la conversacion que un cliente tiene con un tenant o un supplier
        
            query parameters:
                conversation_id (int): el id de la conversacion que se quiere obtener, por defecto esta en all
                con lo que devuelve todas las conversaciones
                
                send_from_message (int): la cantidad de mensajes que se van a cargar iniciando por
                por defecto 0
                
                send_up_to_message (int): la cantidad de mensajes que se van a cargar hasta, si se ingresa send_from
                tambien se debe ingresar este campo
                
                send_from_message and send_up_to_message, hacen un rango de mensajes, es decir, que si 
                send_from_message = 0 and send_up_to_message 20, se van a enviar los primeros 20 mesajes
                en esa conversacion
                
                filter_by (list) (Optional): para filtrar por el tipo de mesaje, por defect is set to "ALL", puedes pasar "EMAIL" and "SMS"
                los string deben ser serparados por coma.
                example:

                filter_by = SMS,EMAIL (sin espacios entre los string a filtrar)
        """
        
        if not user_has_access(request.user, client_id=client_id):
            return Response({'error': 'Access is not valid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        conversation_id = request.GET.get('conversation_id')
        send_from_message = request.GET.get('send_from_message')
        send_up_to_message = request.GET.get('send_up_to_message')
        filter_by:str = request.GET.get('filter_by')
    
        list_to_filter:list = filter_messages_by_via(filter_by=filter_by)
        
        if conversation_id == None:
            conversation = Conversation.objects.filter(client=client_id)
            serializer = ConversationRelatedFieldsSerializer(conversation, many=True)   
            
        else:
            
            try: conversation_id = int(conversation_id)
            except: return Response({'error': 'ValueError: conversation_id debe ser entero'})
            
            if send_from_message is None or send_up_to_message is None:
                send_from_message = 0
                send_up_to_message = 20
            else:
                try:
                    send_from_message = int(send_from_message)
                    send_up_to_message = int(send_up_to_message)
                except:
                    return Response({'error': 'ValueError: send_from_message and send_up_to_message must be integers'})
            
            # here is to return all the messages within a conversation
            
            messages = Message.objects.filter(conversation=conversation_id, vias__in=list_to_filter).order_by('-id')[send_from_message:send_up_to_message]
            serializer = MessageSerializer(messages, many=True)
        
        
        return Response(serializer.data)
            

    def post(self, request, client_id:int):
        
        """Enviar un nuevo mensaje
        
            body parameters:
                conversation (int)(required): el id de la conversacion que se quiere postear
        
        """

        # if email then the message will be sent by email
        
        message = request.data['message']
        subject = request.data['subject']
        
        conversation:Conversation = Conversation.objects.get(id=request.data['conversation'])

        # d = request.data['datetime']
        
        data_for_serializer = {
            'user' : request.user.id,
            'date_time_sent': timezone.now(),
            'subject' : subject,
            'message' : message,
            'sent_by': 'user',
        }
        

        tenant_id = request.data.get('tenant_id')
        supplier_id = request.data.get('supplier_id')
        team_id = request.data.get('team_id')
        
        if tenant_id is not None:
            receiver = 'tenant'
            data_for_serializer['tenant'] = tenant_id
        
            try:
                send_to = Tenants.objects.get(id=tenant_id)
            except Tenants.DoesNotExist:
                return Response(
                    {
                        'error': True, 
                        'message': 'Tenant with selected id does not exist'
                    }, status=status.HTTP_404_NOT_FOUND)


        elif supplier_id is not None:
            receiver = 'supplier'
            data_for_serializer['supplier'] = supplier_id
            
            try:
                send_to = Suppliers.objects.get(id=supplier_id)
            except Suppliers.DoesNotExist:
                return Response(
                    {
                        'error': True, 
                        'message': 'Supplier with selected id does not exist'
                    }, status=status.HTTP_404_NOT_FOUND)
            

        elif team_id is not None:
            receiver = 'team'
            data_for_serializer['team'] = team_id
            
            try:
                send_to = Team.objects.get(id=team_id)
            except Team.DoesNotExist:
                return Response(
                    {
                        'error': True, 
                        'message': 'Team with selected id does not exist'
                    }, status=status.HTTP_404_NOT_FOUND)


        else :
            return Response(
                {
                    'error': True, 
                    'message': 'Enter a valid type id: team_id, tenant_id or supplier_id'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            
        data_for_serializer['receiver'] = receiver
        
        serializer = MessageSerializer(data=data_for_serializer)
        send_by_email = convert_to_bool(request.data['send_by_email'])

        if serializer.is_valid():
            serializer.save()
        
            if send_by_email:
                data_for_serializer['via'] = 'email'
                
                try:
                    SendEmail(
                        send_to = send_to.email,
                        subject = subject,
                        html = f"""
                        <html>
                            <body>
                                <p>{message}</p>
                            </body>
                        </html>
                        """
                    )
                except:
                    return Response(
                        {
                            'error' : True,
                            'message': 'failed while sending the email, please check your internet connection and try again',
                        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                    
                
            else:
                data_for_serializer['via'] = 'phone-sms'
                
                # twilio client
                client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                
                twilio_message =  f"{message}"
                twilio_message = client.messages.create(
                    from_="+19704897499", 
                    to=send_to.phone,
                    body= twilio_message
                )
                
        
            conversation.last_message = message
            conversation.last_message_sent_by_user = message
            conversation.save()
            
            return Response(
                    {
                        'message': 'message sent successfully',
                        'data': serializer.data
                    }, status=status.HTTP_200_OK)
                
        else:
            return Response(
                    {
                        'error' : True,
                        'message': 'serializer is not valid',
                        'message_error' : serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_latest_messages(request, client_id:int):
    """Obtener los mesajes mas recientes, enviados o recibidos
    
    query parameters:
    
        send_from_message (int): la cantidad de mensajes que se van a cargar iniciando por
        por defecto 0
                
        send_up_to_message (int): la cantidad de mensajes que se van a cargar hasta, si se ingresa send_from
        tambien se debe ingresar este campo
        
        received (booleanField) (Optional): indica si se quiere obtener los mensajes enviados o recibidos, por defect is set 
        to True, es decir devuelve los mensajes recibidos
        
        filter_by (list) (Optional): para filtrar por el tipo de mesaje, por defect is set to "ALL", puedes pasar "EMAIL" and "SMS"
        los string deben ser serparados por coma.
        example:

        filter_by = SMS,EMAIL (sin espacios entre los string a filtrar)
    
    Args:
        request (_type_): _description_
        client_id (int): _description_

    Returns:
        _type_: _description_
    """
    
    received:bool = request.GET.get('received')
    send_from_message:int = request.GET.get('send_from_message')
    send_up_to_message:int = request.GET.get('send_up_to_message')
    filter_by:str = request.GET.get('filter_by')
    
    list_to_filter:list = filter_messages_by_via(filter_by=filter_by)

    if received is None:
        received = True
    else:
        try: received = convert_to_bool(received)
        except: return Response({'error': 'ValueError: received debe ser booleanField'})
    
    if send_from_message is None or send_up_to_message is None:
        send_from_message = 0
        send_up_to_message = 20
    else:
        try:
            send_from_message = int(send_from_message)
            send_up_to_message = int(send_up_to_message)
        except:
            return Response({'error': 'ValueError: send_from_message and send_up_to_message deben ser enteros'})
    

    messages = Message.objects.filter(sent_by_user__isnull=received, 
                                      conversation__client=client_id, 
                                      via__in=list_to_filter) \
    .order_by('-id')[send_from_message:send_up_to_message]
  
        
    serializer = MessageSerializer(messages, many=True)  
    return Response(serializer.data)

      
        
@api_view(['POST'])
def twilio_in_bound(request):
    data = dict(request.data.iterlists())
    
    now = timezone.now()
    
    organization:Organization = Organization.objects.get(twilio_number=data['to'])
    
    
    message_serializer = save_message_in_database(
            sent_from=data['from'],
            subject=None, 
            message=data['body'], 
            datetime_received=now,
            sent_from_email=False,
            organization=organization)
    
    return Response(message_serializer)



@api_view(['POST'])
def twilio_in_bound_call(request):
    

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    
    time_in_utc = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)
    client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    # SCHEDULER.add_job(check_status_of_twilio_call, 'interval', seconds=10,
    #                    kwargs={'client': client, 'time_after': time_in_utc})
    
    # SCHEDULER.start()
    

    print('receiving call from Twilio')
    print('--------------------------------')    

    
    return Response({'message': 'success'})



# ----------------------------------------------------

# deprecated from here 

# ----------------------------------------------------


@check_login
def communication_feed(request, token):
    
    user_id = Token.objects.get(key=token).user.id
    
    tenants = Tenants.objects.filter(unit__property_manager=user_id)
    suppliers = Suppliers.objects.filter(landlord=user_id)
    team = Team.objects.filter(landlord=user_id)

    
    return render(
        request, 
        'communications/main_pages/communications-dashboard.html', 
        {
            'tenants': tenants,
            'suppliers': suppliers,
            'team': team,
            'token' : token,
            
        })


@check_login
def messages_details(request, contact_id, user_type, token):

    send_to_team = 'False'
    send_to_tenant = 'False'
    
    if user_type == 'tenant':
        try:
            contact = Tenants.objects.get(id=contact_id)
            send_to_tenant = 'True'
        except:
            return HttpResponse('Not found')

    elif user_type == 'supplier':
        try:
            contact = Suppliers.objects.get(id=contact_id)
            send_to_tenant = 'False'
        except:
            return HttpResponse('Not found')

    elif user_type == 'team':
        try:
            contact = Team.objects.get(id=contact_id)
            send_to_team = 'True'
        except:
            return HttpResponse('Not found')

    
    
    messages = contact.message_set.all().order_by('-date_time_sent')
    messages_sent = messages.count()
    
    return render(
        request, 
        'communications/main_pages/view-messages.html', 
        {
           'contact': contact,
           'send_to_tenant' : send_to_tenant,
           'send_to_team' : send_to_team,
           'messages': messages,
           'messages_sent': messages_sent,
           'token' : token,
        })