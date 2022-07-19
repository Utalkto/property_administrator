# python 

import secrets
import datetime

# django

from django.utils import timezone
from django.core.exceptions import ValidationError

# django rest_framework 
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model # If used custom user model
from django.contrib.auth.password_validation import CommonPasswordValidator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# app modules 
from app_modules.send_email import SendEmail

# models modules
from .models import CustomUser, Organization

# serializer modules
from .serializers import UserSerializer, UserPermissionsSerializser, OrganizationGetSerializer, UserCreateSerializer


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_role(request, format=None):
    data = {'role': request.user.role.role}
    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
def check_if_invited(request, link):
    
    try: organization:Organization = Organization.objects.get(invitation_link=link)
    except: return Response({'invited_by': False})
    
    serializer = OrganizationGetSerializer(organization)
    
    return Response({'invited_by': serializer.data})


@api_view(['PUT'])
@swagger_auto_schema(
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'message': openapi.Schema(type=openapi.TYPE_STRING),
        'file': openapi.Schema(type=openapi.TYPE_FILE),
        'image': openapi.Schema(type=openapi.TYPE_FILE)
    }))
def confirm_user_email(request):
    
    try:
        link = request.data['link']
    except:
        return Response({'error': 'link debe ser ingresado'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    try: 
        user:CustomUser = CustomUser.objects.get(link_to_activate_email=link)
    except CustomUser.DoesNotExist:
        return Response({'error':'CustomUser.DoesNotExist: no hay link asociado a este usuario'})
    
    
    user.link_to_activate_email = None
    user.email_is_actived = True
    
    user.save()
    
    
    return Response({'message': 'success'})
    
# --------------------------------------------------------------
# classes 
# --------------------------------------------------------------


class CustomObtainAuthToken(ObtainAuthToken):
    """Autenticacion de Usuario

    """
    def post(self, request, *args, **kwargs):

        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token:Token = Token.objects.get(key=response.data['token'])

        
        if not token.user.has_access:
            SendEmail(
                send_to='support@utalkto.com',
                subject='new user',
                html='<p>There is an user trying to get into kumbio app but their account is not active</p>'
                )
        
        
        if token.user.organization.payment_status and token.user.email_is_actived:
            return Response(
                {
                    'token': token.key, 
                    'name': token.user.get_full_name(),
                    'active': token.user.has_access,
                    'user_permissions': UserPermissionsSerializser(token.user).data
                })
            
        else:
            if token.user.role == 2:
                return Response({
                    'message': 'Your account is inactive since your plan has experied, please renew your plan to access again'
                }, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                
                if not token.user.email_is_actived:
                    
                    return Response(
                    {
                        'message': 'You have to confirm your email to continue',
                        
                    }, status=status.HTTP_401_UNAUTHORIZED
                    )
                    
                else:
                
                    return Response(
                        {
                            'message': 'Access denied',
                            
                        }, status=status.HTTP_401_UNAUTHORIZED
                    )
    

class CreateUserView(CreateAPIView):
    """Crea Usuarios

    """
    
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserCreateSerializer
    

class RecoverPasswordAPI(APIView):
    
    
    def get(self, request):
        
        """Para ver si este es un link es valido 
        
        query parameters :
            link (str) : el link que se va a validar a ver si es valido este link 
        """
        
        try:
            user:CustomUser = CustomUser.objects.get(link_to_recover_password=request.GET['link'])
        except KeyError:
            return Response({'error': 'KeyError: link debe ser enviada como query parameter'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'CustomUser.DoesNotExist: no hay ningun usuario que tenga este link registrado'}, 
                            status=status.HTTP_404_NOT_FOUND)
            
        
        now = timezone.now()
        four_hours_before = now - datetime.timedelta(hours=4)
        
        user.link_to_recover_password = None
        user.time_recover_link_creation = None
        user.save()
        
        if four_hours_before > user.time_recover_link_creation:
            return Response({'error':'Este link ha expirado'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        
        user_serializer = UserSerializer(user)
        return Response({'user_id': user_serializer.data['id']}) 
                
    
    def post(self, request):
        
        """Para pedir la peticion de reestablecer la password,

        body_parameters :
            email (EmailField) : el email de la persona que quiere reestablecer la password
        
        """
        
        try:
            user:CustomUser = CustomUser.objects.get(email=request.data['email'])
        except KeyError:
            return Response({'error': 'KeyError: email debe ser enviada como body parameter'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'CustomUser.DoesNotExist: no hay ningun usuario que tenga este correo registrado'}, 
                            status=status.HTTP_404_NOT_FOUND)
            
        
        user.link_to_recover_password = secrets.token_urlsafe(26)
        user.time_recover_link_creation = timezone.now() 
        
        html = f'<h1> This is your link to restore your password </h1> \
        <p>This link will be valid for only 4 hours </p> \
        <a href=http://localhost:3000/recover-password/{user.link_to_recover_password}> Restore my password'
        
        # send email here
        try:
            SendEmail(
                send_to=user.email,
                subject="Restore Password",
                html= html
            )
        except:
            return Response({'error': 'error sending the email to the user'})
        
        user.save()
        
        return Response({'message': 'success'})
    
    
    def put(self, request):
        """Cambiar la password del user
        
        bory parameters :
            user_id (id) (required) : el id del usuario del que se va a cambiar la password
            password (str) (required) : la nueva password que el usuario quiere poner

        Args :
            request (_type_): _description_
        """
        
        user:CustomUser = CustomUser.objects.get(id=int(request.data['user_id']))
        
        try:
            password = request.data['password']
        except:
            return Response({'error': 'password debe ser pasada como body parameter'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        
        if len(password) < 8:
            return Response({'error': 'la password debe tener 8 o mas caracteres'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        
        validator = CommonPasswordValidator()
        
        try:
            validator.validate(password=password)
        except ValidationError:
            return Response({'error': 'ValidationError: la password dada es muy comun'})
            
        
        user.set_password(password)
        user.save()
        return Response({'message': 'success'})
        
        