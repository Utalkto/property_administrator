# Python 3.8.0
from imap_tools import MailBox, A
from cryptography.fernet import Fernet
from communications.models import Conversation

import datetime

# django
from properties.models import Tenants
from register.models import Organization

from django.db.models import Q

from tickets.models import Suppliers
from .serializers import MessageSerializer, ConversationSerializer, ConversationRelatedFieldsSerializer


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


def save_email_in_database(sent_from:str, subject:str, message:str, datetime_received:datetime):
    
    # we need to check if the email that was sent to the organization is from a contact that is in the db
    
    data_for_serializer = {
        'date_time_sent' : datetime_received,
        'subject': subject,
        'message': message,
        'via': 'EMAIL',
    }
    
    try: 
        tenant:Tenants = Tenants.objects.get(Q(email=sent_from) | Q(email2=sent_from))
        data_for_serializer['tenant'] = tenant.id
        data_for_serializer['client'] = tenant.client.id
        try:
            conversation:Conversation = Conversation.objects.get(tenant_id=tenant.id)
            
        except:
            print('creating a new conversatoin in the db for tenant')
            conversation = create_new_conversation(tenant_id=tenant.id, client_id=tenant.client.id)
            print(conversation)
        
    except:
        try: 
            supplier:Suppliers = Suppliers.objects.get(email=sent_from)
            data_for_serializer['supplier'] = supplier.id
            data_for_serializer['client'] = supplier.client.id
            
            try:
                conversation:Conversation = Conversation.objects.get(supplier=supplier.id)

            except:
                print('creating a new conversatoin in the db for supplier')
                conversation = create_new_conversation(supplier_id=supplier.id, client_id=supplier.client.id)
            
        except:
            data_for_serializer['unknown_email'] = sent_from
            conversation = None
    
    if conversation:
        data_for_serializer['conversation'] = conversation.id
        conversation.last_message = message
        conversation.last_message_sent_by_user = False
    else:
        data_for_serializer['conversation'] = None
    
    
    conversation.save()
    
    
    serializer = MessageSerializer(data=data_for_serializer)
    
    
    if serializer.is_valid():
        serializer.save()
    

def get_emails(email:str, password:str):
    # get emails that have been received since a certain time
    with MailBox(SMTP_SERVER).login(email, password, 'INBOX') as mailbox:
        for msg in mailbox.fetch(A(date_gte=datetime.date(2022, 6, 23))):
            
            t = msg.date.time()
            now = datetime.datetime.now()
            forty_seconds_before = now - datetime.timedelta(seconds=60)       
            
            if t > forty_seconds_before.time():
                
                print(msg.subject)
                
                save_email_in_database(
                    sent_from=msg.from_,
                    subject=msg.subject, 
                    message=msg.text, 
                    datetime_received=msg.date)
                

def check_organization_emails():
    
    print('getting emails')
    
    organizations = Organization.objects.all()
    
    for org in organizations:
        email_password = get_password(org)
        
        # the emails get save in this function 
        get_emails(org.email_username, email_password)
    
    
    