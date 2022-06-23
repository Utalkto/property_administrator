# python
import datetime

# django 

from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# twilio 
from twilio.rest import Client

from communications.models import Conversation, Message

# serializers

from .serializers import ConversationSerializer, MessageSerializer
from .models import Message
from django.utils import timezone

# property modules

from properties.models import Tenants, Team
from tickets.models import Suppliers

# same app modules 
from app_modules.send_email import SendEmail
from app_modules.decorators import check_login
from app_modules.main import convert_to_bool

# API -----------------------------------------------

class CommunicationsAPI(APIView):
    
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
        """
        
        conversation_id = request.GET.get('conversation_id')
        send_from_message = request.GET.get('send_from_message')
        send_up_to_message = request.GET.get('send_up_to_message')
        
        
        if conversation_id == None:
            conversation = Conversation.objects.filter(client=client_id)         
            return ConversationSerializer(conversation)
            
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
            
            messages = Message.objects.filter(conversation=conversation_id)[send_from_message:send_up_to_message]
             
            return MessageSerializer(messages).data
            

    def post(self, request):

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
                
                
                # Twilio settings 
                # this must change to the app twilio account
                account_sid = "AC169f0dd1f79d9a78e183de54363307bb" 
                auth_token  = "15c699a3cf3f29fcc776a47259e58593"

                # twilio client
                client = Client(account_sid, auth_token)
                
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





    
