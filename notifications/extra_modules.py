# django 

from django.utils import timezone

from notifications.serializers import NotificationSerializer
from register.models import CustomUser, Organization, OrganizationClient

from app_modules.send_email import SendEmail
from properties.models import Property, Tenants, Unit
from tickets.models import Suppliers

# notifications can be send to more than one user at a time

NOTIFICATION_TEXTS = {
    'NEW_MESSAGE': {
        'subject': 'Your got a new message', 
        'html': '<p>You got a new mesage from {message_sender}</p>', 
        'text': 'Your got a new message from {message_sender}'
    },
    
    'NEW_SMS': {
        'subject': 'Your got a new email', 
        'html': '<p>You got a new mesage from {message_sender}</p>', 
        'text': 'Your got a new email from {contact_type} {contact_name}'
    },
    
}


def create_notification(users:list, client:OrganizationClient, notification_type:int, message_sender:CustomUser=None,
                        tenant:Tenants=None, supplier:Suppliers=None,
                        send_to_email:bool=False, send_to_landlords:bool=False, 
                        send_to_organization_admins:bool=False) -> bool:
    
    """Create a new notification

    notification_type must be one of these
        1: NEW_MESSAGE,
        2: NEW_TICKET_OPENED,
        3: NEW_SMS,
        4: NEW_EMAIL,
    
    
    Args:
        users (list): a list of users that are going to received the notification
        type (int): _description_
    """

    NOTIFICATION_TYPE = {
        1: 'NEW_MESSAGE',
        2: 'NEW_TICKET_OPENED',
        3: 'NEW_SMS',
        4: 'NEW_EMAIL',
    }
    
    assert notification_type in NOTIFICATION_TYPE.keys(), 'notification_type parameter must be \
    1:NEW_MESSAGE, 2:NEW_TICKET_OPENED, 3:NEW_SMS, 4:NEW_EMAIL'
    
    try:
        user[0]
    except IndexError:
        raise 'when passing send_to_landlords then at least a user must be included'
    

    
    
    if notification_type == 1:
        notification_text:str = NOTIFICATION_TEXTS[notification_type]['text']\
        .replace('{mesage_sender}', message_sender.get_full_name())
    elif notification_type == 3: 
        
        if tenant:
            contact_type = 'tenant'
            contact_name = tenant.name
        elif supplier:
            contact_type = 'tenant'
            contact_name = supplier.name
        
    
        notification_text:str = NOTIFICATION_TEXTS[notification_type]['text']\
        .replace('{contact_type}', contact_type).replace('{contact_name}', contact_name)
    
    
    data_for_serializer = {
        'client_id': client.id,
        'notification_type': NOTIFICATION_TYPE[notification_type],
        'created_date': timezone.now(),
        'notification': notification_text, 
        'send_to_email': send_to_email,
        }
    
    html_part = NOTIFICATION_TEXTS[notification_type]['html'].replace('{mesage_sender}', message_sender.get_full_name())
    email_subject = NOTIFICATION_TEXTS[notification_type]['subject']
    
    
    for user in users:
        
        data_for_serializer['user'] = user.id
        
        serializer = NotificationSerializer(data=data_for_serializer)
        
        if serializer.is_valid():
            serializer.save()
        else:
            raise serializer.errors
        
        if send_to_email:
            
            try:
                SendEmail(
                    send_to=user.email,
                    subject=email_subject,
                    html=html_part
                )
            except:
                return False
            
    
    
    if send_to_landlords:
        landlords = CustomUser.objects.filter(Organization=client.organization.id, role__role="LANDLORD")
        landlords_with_access = list()
        
        for landlord in landlords:
            if landlord.clients_access.keys():
                landlords_with_access.append(landlord)    
        
        for landlord in landlords_with_access:
            data_for_serializer['user'] = landlord.id
            
            serializer = NotificationSerializer(data=data_for_serializer)
            
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializer.errors
            
        try:
            SendEmail(
                send_to=user.email,
                subject=email_subject,
                html=html_part
            )
        except:
            return False
    
    
    if send_to_organization_admins:
        
        admins = CustomUser.objects.filter(organization=client.organization.id)
        
        for admin in admins:
            data_for_serializer['user'] = admin.id
            
            serializer = NotificationSerializer(data=data_for_serializer)
            
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializer.errors
            
        
        if send_to_email:
            try:
                SendEmail(
                    send_to=user.email,
                    subject=email_subject,
                    html=html_part
                )
            except:
                return False
            
            
    return True
            
            
    