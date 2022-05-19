# python

import datetime


# django 

from django.shortcuts import render
from django.http import HttpResponse


from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# wilio 

from twilio.rest import Client

# serializers

from .serializers import MessageSerializer

# property modules

from properties.models import Tenants

# same app modules 

from app_modules.send_email import SendEmail


# other funtions

def convert_to_bool(value):
    if type(value) == str:
        value = value.upper()
    
    if value in ['FALSE', 0, None]:
        return False
    
    return True

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
        
        try:
            tenant = Tenants.objects.get(id=int(request.data['person_id']))
        except Tenants.DoesNotExist:
            return Response(
                {
                    'error': True, 
                    'message': 'Tenant with selected id does not exist'
                }, status=status.HTTP_404_NOT_FOUND)
            
        data_for_serializer = {
            'destinatary': tenant.id,
            'sent_by' : request.user.id,
            'date_time_sent': datetime.datetime.now(),
            'subject' : subject,
            'message' : message
        }
        
        serializer = MessageSerializer(data=data_for_serializer)
        
        
        send_by_email = convert_to_bool(request.data['send_by_email'])
        
        
        if send_by_email:
            
            destinatary_email = tenant.email
            data_for_serializer['via'] = 'email'
            
            try:
                SendEmail(
                    send_to = destinatary_email,
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
            destinatary_phone = tenant.phone
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
                to=destinatary_phone,
                body= twilio_message
            )
            
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {
                        'message': 'message sent successfully'
                    }, status=status.HTTP_200_OK)
                
        else:
            return Response(
                    {
                        'error' : True,
                        'message': 'serializer is not valid',
                        'message_error' : serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
          
        
# ----------------------------------------------------


def communication_feed(request):
    return HttpResponse('here is your response, my friend')






    
