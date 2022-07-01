# Python 3.8.0
from imap_tools import MailBox, A
from cryptography.fernet import Fernet
from communications.models import Conversation

import datetime

# django
from properties.models import Tenants
from register.models import CustomUser, Organization, OrganizationClient

from django.db.models import Q

from tickets.models import Suppliers
from .serializers import MessageSerializer, ConversationSerializer, ConversationRelatedFieldsSerializer

from notifications.extra_modules import create_notification


FROM_PWD = "OrinocoV2022.." 
FROM_PWD = "AMelendes2022$" 


ORG_EMAIL = "@orinocoventures.com" 
ORG_EMAIL = "@utalkto.com" 


FROM_EMAIL = "amelendes" + ORG_EMAIL 
SMTP_SERVER = "imap.hostinger.com" 

SMTP_PORT = 993


def create_new_conversation(client_id:int, tenant_id:int=None, supplier_id:int=None) -> Conversation:
    
    data_for_serializer = {
        'tenant': tenant_id,
        'supplier_id': supplier_id,
        'client': client_id,
    }
    
    serializer = ConversationSerializer(data=data_for_serializer)
    
    if serializer.is_valid():
        serializer.save()
    
    else:
        print('---------------------------------')
        print(serializer.errors)
        print('---------------------------------')
    
    
    return Conversation.objects.get(id=serializer.data['id'])
    

def get_password(organization:Organization) -> str:

    f = Fernet(organization.key.tobytes())

    email_paswword = f.decrypt(organization.email_password.tobytes()).decode('utf-8')
    
    return email_paswword


def save_message_in_database(sent_from:str, subject:str, message:str, datetime_received:datetime,
                            organization:Organization=None, sent_from_email:bool=True) -> dict:
    
    # we need to check if the email that was sent to the organization is from a contact that is in the db
    
    data_for_serializer = {
        'date_time_sent' : datetime_received,
        'subject': subject,
        'message': message,
    }
    
    client:OrganizationClient = None
    
    if sent_from_email:
        data_for_serializer['via'] = 'EMAIL'
    else:
        data_for_serializer['via'] = 'SMS'

    try: 
        if sent_from_email:
            tenant:Tenants = Tenants.objects.get(Q(email=sent_from) | Q(email2=sent_from))
        else:
            tenant:Tenants = Tenants.objects.get(Q(phone=sent_from) | Q(phone2=sent_from))
        
        client = tenant.client
        organization = client.organization
        
        data_for_serializer['tenant'] = tenant.id
        data_for_serializer['client'] = client.id
        
        try:
            conversation:Conversation = Conversation.objects.get(tenant_id=tenant.id)
        except:
            print('creating a new conversation in the db for tenant')
            conversation = create_new_conversation(tenant_id=tenant.id, client_id=tenant.client.id)
            print(conversation)
        
    except Tenants.DoesNotExist:
        try: 
            if sent_from_email:
                supplier:Suppliers = Suppliers.objects.get(email=sent_from)
            else:
                supplier:Suppliers = Suppliers.objects.get(phone=sent_from)
                
            data_for_serializer['supplier'] = supplier.id
            data_for_serializer['client'] = supplier.client.id
            
            
            organization = supplier.organization
            
            try:
                conversation:Conversation = Conversation.objects.get(supplier=supplier.id)

            except:
                print('creating a new conversatoin in the db for supplier')
                conversation = create_new_conversation(supplier_id=supplier.id, client_id=supplier.client.id)
            
        except:
            if sent_from_email:
                data_for_serializer['unkonwn_email'] = sent_from
            else:
                data_for_serializer['unkonwn_phone'] = sent_from
            
            conversation = None
    
    if conversation:
        data_for_serializer['conversation'] = conversation.id
        conversation.last_message = message
        conversation.last_message_sent_by_user = False
        conversation.save()
        
    else:
        data_for_serializer['conversation'] = None
       
    
    serializer = MessageSerializer(data=data_for_serializer)
    
    if serializer.is_valid():
        
        # create notification
        users_with_access = list()
        
        if client:
            users = CustomUser.objects.filter(organization=client.organization.id)
            
            for user in users:
                if client.id in user.clients_access.keys():
                    users_with_access.append(user)
            
        elif organization:
            users = CustomUser.objects.filter(organization=organization.id)
            users_with_access = users
            
        create_notification(users=users_with_access, client=client, notification_type=4, tenant=tenant)
        # ---------------------------------------------------------------
        
        serializer.save()
    else:
        print(serializer.errors)
        
    return dict(serializer.data)
    

def get_emails(email:str, password:str, organization:Organization):
    # get emails that have been received since a certain time
    
    now = datetime.datetime.now()
    
    with MailBox(SMTP_SERVER).login(email, password, 'INBOX') as mailbox:
        for msg in mailbox.fetch(A(date_gte=datetime.date(now.year, now.month, now.day))):
            
            t = msg.date.time()
            forty_seconds_before = now - datetime.timedelta(seconds=60)       
            
            if t > forty_seconds_before.time():
                
                print(msg)
                print(msg.subject)
                
                save_message_in_database(
                    sent_from=msg.from_,
                    subject=msg.subject, 
                    message=msg.text, 
                    datetime_received=msg.date,
                    organization=organization)
                

def check_organization_emails():
    
    print('getting emails')
    
    organizations = Organization.objects.all()
    
    for org in organizations:
        email_password = get_password(org)
        
        # the emails get save in this function 
        get_emails(org.email_username, email_password, org)
    
    
    