from rest_framework import status

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import CustomUser

from app_modules.send_email import SendEmail
    

@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_role(request, format=None):
    data = {'role': request.user.role.role}
    return Response(data, status=status.HTTP_200_OK)



class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        
        # try:
        #     username = CustomUser.objects.get(email__iexact=request.data['email']).username
            
        # except CustomUser.DoesNotExist:
            
        #     return Response({
        #         "non_field_errors": [
        #             "Unable to log in with provided credentials. here" 
        #         ]
        #     })
        
        
        # request.data['username'] = username
        
        print('-----------------------------------')
        print(request.data)
        print('-----------------------------------')

        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        
        if not token.user.has_access:
            SendEmail(
                send_to='support@utalkto.com',
                subject='new user',
                html='<p>There is a user trying to get into kumbio app but its account is not active</p>'
                )
        


        return Response(
            {
                'token': token.key, 
                'name': token.user.get_full_name(), 
                'active': token.user.has_access
            })
    
