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

# twilio 
from twilio.rest import Client

# serializers

from .serializers import MessageSerializer

# property modules

from properties.models import Tenants
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
    

    def post(self, request):

        # if email then the message will be sent by email
        
        message = request.data['message']
        subject = request.data['subject']
        
        data_for_serializer = {
            'user' : request.user.id,
            'date_time_sent': datetime.datetime.now(),
            'subject' : subject,
            'message' : message,
            
            'sent_by': 'user',
        }
        

        tenant_id = request.data.get('tenant_id')
        supplier_id = request.data.get('supplier_id')
        
        if tenant_id is None:
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
            
        else:
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
                
            
        data_for_serializer['receiver'] = receiver
        
        serializer = MessageSerializer(data=data_for_serializer)
        send_by_email = convert_to_bool(request.data['send_by_email'])
        
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
            
            twilio_message =  f"Subject: {subject}. Message: {message}"
            twilio_message = client.messages.create(
                from_="+19704897499", 
                to=send_to.phone,
                body= twilio_message
            )
            
        
        
        if serializer.is_valid():
            serializer.save()
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

    t = Tenants.objects.filter(unit__property_manager=request.user.id)
    
    return render(
        request, 
        'communications/main_pages/communications-dashboard.html', 
        {
            'tenants': t,
            'token' : token,
            
        })


@check_login
def messages_details(request, tenant_id, token):
    
    try:
        tenant = Tenants.objects.get(id=tenant_id)
    except Tenants.DoesNotExist:
        return HttpResponse('The user requested does not exist')
    
    
    messages = tenant.messagesent_set.all().order_by('-date_time_sent')
    messages_sent = messages.count()
    
    
    return render(
        request, 
        'communications/main_pages/view-messages.html', 
        {
           'tenant': tenant,
           'messages': messages,
           'messages_sent': messages_sent,
           'token' : token,
        })





    
