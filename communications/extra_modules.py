# Python 3.8.0

import imaplib
import email
import traceback 
from imap_tools import MailBox, A
import datetime
from cryptography.fernet import Fernet
# django
from django.utils import timezone
from register.models import Organization


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
        
def save(self, **kwargs):        
    f = Fernet(self.key)
    self.email_password = f.encrypt(self.email_password)
    super().save(**kwargs)
    
    

def get_password(organzation:Organization):
    
    f = Fernet(organzation.key)
    email_paswword = f.decrypt(organzation.email_password).decode('utf-8')
    
    
    return email_paswword

def check_organization_emails():
    
    organizations = Organization.objects.all()
    
    for org in organizations:
        email_password = get_password(org)
    
    # decoding the password email for that client 
    



def get_emails():
    # get emails that have been received since a certain time
    with MailBox(SMTP_SERVER).login(FROM_EMAIL, FROM_PWD, 'INBOX') as mailbox:
        for msg in mailbox.fetch(A(date_gte=datetime.date(2022, 6, 21))):
            
            t = msg.date.time()
            now = datetime.datetime.now()
            twenty_seconds_before = now - datetime.timedelta(seconds=360)       
            
            if t > twenty_seconds_before.time():
                print('subject:', msg.subject)
                print('message:', msg.text)
            
            
            
        
    
    
    