from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import smtplib, ssl

class SendEmail:
    def __init__(self, send_to:str, subject:str, html:str, attach_file=None) -> str:
        
        self.send_to = send_to
        self.subject = subject
        self.html = html
        self.attach_file = attach_file
        
        self.send_email(send_to=self.send_to, subject=self.subject, html=self.html, attach_file=self.attach_file)                
    
    
    def send_email(self, send_to:str, subject:str, html:str, attach_file):
        # email settings
        email_message = MIMEMultipart('alternative')
        email_message['Subject'] = subject
        email_message['From']='hello@orinocoventures.com'
        email_message['To']= send_to
        
        if 'hostinger' not in send_to:
            html_part = MIMEText(html,'html')
            email_message.attach(html_part)

        
        if attach_file is not None:
            attach = MIMEBase('application', 'octet-stream')
            attach.set_payload(open(attach_file, 'rb').read())
            encoders.encode_base64(attach)
            attach.add_header('content-Disposition',f'attachment; filename={attach_file}')
            
            email_message.attach(attach)

        # gmail app password : xbttxlrqhiwrdxux
        context = ssl.create_default_context()
        
        # we try to send the email
        try:
            with smtplib.SMTP_SSL("smtp.hostinger.com", 465, context=context) as server:
                server.login("hello@orinocoventures.com",'OrinocoV2022..' )
                
                server.sendmail(
                    from_addr="hello@orinocoventures.com", 
                    to_addrs=send_to,
                    msg=email_message.as_string())
        except:
            # if it fails then we try one moretime
            try:
                with smtplib.SMTP_SSL("smtp.hostinger.com", 465, context=context) as server:
                    server.login("hello@orinocoventures.com",'OrinocoV2022..' )
                    
                    server.sendmail(
                        from_addr="hello@orinocoventures.com", 
                        to_addrs=send_to,
                        msg=email_message.as_string())
            # if it fails again then we raise and exception and the site where the class is being called must 
            # handle the error
            except:
                raise Exception('Cannot send email')
        



