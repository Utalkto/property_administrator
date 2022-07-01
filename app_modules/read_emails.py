# Python 3.8.0
import datetime
import imaplib
import email
import traceback 

from properties.models import Tenants
from payments.models import UnitPayments

# my_gemail_password = 'pvoonwxleegwinxr'
# server.login("hello@orinocoventures.com",'OrinocoV2022..' )
FROM_PWD = "OrinocoV2022.." 
FROM_PWD = "AMelendes2022$" 

ORG_EMAIL = "@orinocoventures.com" 
ORG_EMAIL = "@utalkto.com" 

FROM_EMAIL = "amelendes" + ORG_EMAIL 
SMTP_SERVER = "imap.hostinger.com" 
SMTP_PORT = 993


def save_email_in_data_base(tenant_email:str, payment_amount:float, reference_number:str, email_date:str):
    
    unit = Tenants.objects.get(email=tenant_email).unit
    
    unit.debt -= payment_amount
    unit.save()
    
    
    UnitPayments(
        unit = unit,
        payment_date= datetime.datetime.strptime(email_date, '%Y-%m-%d'),
        payment_method = 'Transfer',
        payment_amount = payment_amount,
        reference_number = reference_number,
        ).save()
    


def read_email():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        
        # data = mail.search(None, '(FROM "notify@payments.interac.ca")')
        data = mail.search(None, '(FROM "hello@orinocoventures.com")')
        
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        
        deposit_amount = '' # string at first but then will need to parse it to int
        refence_number = ''
        objective_string = 'Reference Number: '
        objective_please = 'esaelP'
        
        current_index = 0
        
        # iterating throught each email_id
        for i in id_list:
            data = mail.fetch(str(int(i)), '(RFC822)' )
            
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = str(msg['subject'])
                    
                    if 'INTERAC e-Transfer: A money transfer from' in email_subject:
                        tenant_email = str(msg['reply-to'])
                        email_date = str(msg['date'])
    
                        email_message = str(msg.get_payload()[0])
                        
                        get_amount:bool = False
                        get_reference:bool = False
                        
                        current_word:str = ''
                        
                        for w in email_message:
                            
                            # code to get the amount of the deposit
                            
                            if w == '' and get_amount or w == ' ' and get_amount:
                                deposit_amount = float(deposit_amount)
                                get_amount = False
                                
                            if get_amount:
                                deposit_amount += w
                                
                            if w == '$' and not get_amount:
                                get_amount = True
                                
                            # code to get the reference number
                               
                            if w == '' and get_reference or w == ' ' and get_reference:                               
                                    
                                get_reference = False

                                # removing "please" part
                                current_word = ''
                                for i in range(len(refence_number) - 1, 0, - 1):                                    
                                    
                                    if current_word == objective_please:
                                        refence_number = refence_number[:i].strip()
                                        save_email_in_data_base(
                                            tenant_email, 
                                            deposit_amount, 
                                            refence_number, 
                                            email_date)
                                             
                                        return
                                    
                                    current_word += refence_number[i]
                            
                            if get_reference:
                                refence_number += w
                              
                            
                            if not get_reference and w == objective_string[current_index]:
                                current_word += w
                                current_index += 1
                                
                                if current_word == objective_string:
                                    get_reference = True
                                
                            else:
                                current_word = ''
                                current_index = 0
                                                         
    except Exception as e:
        traceback.print_exc() 
        print(str(e))
