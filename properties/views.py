# python 
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import jwt
import smtplib, ssl

# twilio 
from twilio.rest import Client

# django 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

# models 
from properties.models import Properties, Units
from properties.serializers import PropertiesSerializer, TenantSerializer, UnitsSerializer
from register.models import CustomUser





@api_view(['POST'])
def vacantUnit(request, id):

    unit = Units.objects.get(id=id)
    unit.rented = not unit.rented
    unit.save()
    serializer = UnitsSerializer(unit)


    #COMUNICACION POR MENSAJE DE TEXTO
    if unit.rented:
        return Response({"unit": serializer.data})
    else:
        account_sid = "ACe61e701812ddfb138275589f4a556d35"
        auth_token  = "7c25fe7f3dc40bab21cef73caba5065a"

        client = Client(account_sid, auth_token)

        mensaje =   f"{unit.name} entro en proceso de desalojo"
        message = client.messages.create(
            from_="+19035224352", 
            to="+584120148704",
            body= mensaje
        )
        
        #COMUNICACION POR EMAIL
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = 'Move-out Instructions'
        mensaje['From']='hello@orinocoventures.com'
        mensaje['To']='acampos@utalkto.com'
        html = f"""
        <html>
            <body>
                <h1>Eviction instructions</h1>
          
            </body>

        </html>

        """
        parte_html = MIMEText(html,'html')
        mensaje.attach(parte_html)

        # AJUNTANDO ARCHIVO DE DESALOJO
        ajunto = MIMEBase('application', 'octet-stream')
        ajunto.set_payload(open('test.pdf', 'rb').read())
        encoders.encode_base64(ajunto)
        ajunto.add_header('content-Disposition','attachment; filename="test.pdf"')
        mensaje.attach(ajunto)


        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.hostinger.com", 465, context=context) as server:
            server.login("hello@orinocoventures.com",'Orinoco2022..' )
            server.sendmail(from_addr="hello@orinocoventures.com", to_addrs="acampos@utalkto.com",msg=mensaje.as_string() )


        return Response({"unit": serializer.data})


class PropertiesViewSet(APIView):

    def post(self, request):

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            
            try: 
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                landlord = CustomUser.objects.get(id=token['id'])
                request.data['landlord'] = landlord.id

                serializer =  PropertiesSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'error':False, "mensaje": "propiedad registrada"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': True, 'mensaje': 'Error al registrar propiedad'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            except CustomUser.DoesNotExist:
                return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)
    
            except:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_401_UNAUTHORIZED)
           
        else:
            Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED)   
    
    
    def put(self, request, id):

       
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                propertie = Properties.objects.get(id=id)
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                landlord = CustomUser.objects.get(id=token['id'])
                request.data['landlord'] = landlord.id
                propertie = PropertiesSerializer(instance=propertie, data=request.data)

                if propertie.is_valid():
                    propertie.save()
                    return Response(propertie.data)
                else:
                    return Response(propertie.errors)

            except Properties.DoesNotExist:
                return Response({'error': True, 'mensaje': 'propiedad no existente'}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED) 
    
    
    def get(self,request):

        if 'Authorization' in request.headers and request.headers != '' :
            token = request.headers['Authorization']
            try:
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                serializer = PropertiesSerializer(Properties.objects.filter(landlord = token['id']), many=True)
                return Response(serializer.data)
               
            except:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_402_PAYMENT_REQUIRED)

        else:
            Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED) 
    
    
    def delete(self, request,id):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                propertie = Properties.objects.get(id=id)
                propertie.delete()
                return Response({'error':False, "mensaje": "propiedad eliminada satifactoriamente"}, status=status.HTTP_201_CREATED)
            except Properties.DoesNotExist:
                return Response({'error': True, 'mensaje': 'propiedad no existente'}, status=status.HTTP_404_NOT_FOUND)
            except jwt.exceptions.InvalidTokenError:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED)   

     
class  UnitsViewSet(APIView):
    
    def post(self, request):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try: 
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                landlord =  CustomUser.objects.get(id=token['id'])
                request.data['landlord'] = landlord.id
                propertie = Properties.objects.get(id=request.data['landlord'])
                serializer =  UnitsSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'error':False, "mensaje": "propiedad registrada"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': True, 'mensaje': 'Error al registrar propiedad', 'error': serializer.errors}, status=status.HTTP_402_PAYMENT_REQUIRED)
            except CustomUser.DoesNotExist:
                return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)
    
            except:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_401_UNAUTHORIZED)
           
        else:
            Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED) 
    
    def put(self, request, id):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                unit = Units.objects.get(id=id)
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                landlord = CustomUser.objects.get(id=token['id'])
                request.data['landlord'] = landlord.id
                serializer = UnitsSerializer(instance=unit, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)

            except Units.DoesNotExist:
                return Response({'error': True, 'mensaje': 'unidad no existente'}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self,request,id):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                units = Units.objects.filter(properties_id=id , landlord_id=token['id'])
                serializer = UnitsSerializer(units, many=True)
                return Response(serializer.data)
              
            except Units.DoesNotExist:
                return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)
    
            except:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_401_UNAUTHORIZED)
           
        else:
            Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, id):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                unit = Units.objects.get(id=id)
                unit.delete()
                return Response({'error':False, "mensaje": "unidad eliminada satifactoriamente"}, status=status.HTTP_201_CREATED)
            except Units.DoesNotExist:
                return Response({'error': True, 'mensaje': 'unidad no existente'}, status=status.HTTP_404_NOT_FOUND)
            except jwt.exceptions.InvalidTokenError:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED) 



class TenantViewSet(APIView):
    def post(self, request):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try: 
                token  = jwt.decode(token, "123456", algorithms=["HS256"])
                landlord =  CustomUser.objects.get(id=token['id'])
                request.data['landlord'] = landlord.id
                serializer =  TenantSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'error':False, "mensaje": "tenant registrada"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': True, 'mensaje': 'Error al registrar tenant', 'error': serializer.errors}, status=status.HTTP_402_PAYMENT_REQUIRED)
            except CustomUser.DoesNotExist:
                return Response({'error': True, 'usuario ': ''}, status=status.HTTP_401_UNAUTHORIZED)
    
            except:
                return Response({'error':True,'mensaje': 'Invalid Token',},status=status.HTTP_401_UNAUTHORIZED)
           
        else:
            Response({'error': True, 'mensaje': 'credentials required'}, status=status.HTTP_401_UNAUTHORIZED) 


        