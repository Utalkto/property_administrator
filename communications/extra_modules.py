# Python 3.8.0

import imaplib
import email
import traceback 
from imap_tools import MailBox, A
import datetime
from cryptography.fernet import Fernet
# django
from properties.models import Tenants
from register.models import Organization

from django.db.models import Q

from tickets.models import Suppliers
from .serializers import MessageSerializer


FROM_PWD = "OrinocoV2022.." 
FROM_PWD = "AMelendes2022$" 


ORG_EMAIL = "@orinocoventures.com" 
ORG_EMAIL = "@utalkto.com" 


FROM_EMAIL = "amelendes" + ORG_EMAIL 
SMTP_SERVER = "imap.hostinger.com" 

SMTP_PORT = 993

# deprecated ??? 
def read_emails():
    try:

        mail = imaplib.IMAP4_SSL(SMTP_SERVER)

        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        # data = mail.search(None, '(FROM "notify@payments.interac.ca")')

        data = mail.search(None, '(FROM "andresruse18@gmail.com")')
        mail_ids = data[1]

        id_list = mail_ids[0].split()
        
        # iterating throught each email_id
        n = 0
        for i in id_list:
            n+=1
            data = mail.fetch(str(int(i)), '(RFC822)')

            for response_part in data:
                arr = response_part[0]

                if isinstance(arr, tuple):

                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = str(msg['subject'])
                    
                    email_message = str(msg.get_payload()[0])
    
                    print('-----------------------------------')
                    print('-----------------------------------')
                    
                    print('subject:', email_subject)
                    print('message:', email_message)
                    print('times:', n)
                    
                    print('-----------------------------------')
                    print('-----------------------------------')
            break
                            
    except Exception as e:

        traceback.print_exc() 

        print(str(e))


# we need to check each oraganizatio email to be able to get all them and send them to the correct place
        
# def save(self, **kwargs):        
#     f = Fernet(self.key)
#     self.email_password = f.encrypt(self.email_password)
#     super().save(**kwargs)
    
    

def get_password(organization:Organization):

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
        tenant = Tenants.objects.get(Q(email=sent_from) | Q(email2=sent_from))
        data_for_serializer['tenant'] = tenant.id
        data_for_serializer['client'] = tenant.client.id
        
    except:
        try: 
            supplier = Suppliers.objects.get(email=sent_from)
            data_for_serializer['supplier'] = supplier.id
            data_for_serializer['client'] = supplier.client.id
            
        except:
            data_for_serializer['unknown_email'] = sent_from
            
            
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
    
    
    