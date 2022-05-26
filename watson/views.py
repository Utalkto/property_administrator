from rest_framework.views import APIView
from rest_framework.response import Response

from app_modules.send_email import SendEmail
from properties.models import Tenants
from properties.serializers import TenantSerializer
from .serializers import ProductSerializer

from rest_framework import status
from app_modules.send_email import SendEmail

from uuid import uuid4

class WatsonApi(APIView):
    
    def post(self, request):


        serializer = ProductSerializer(data=request.data)

        email = request.data['email']

        request.data['product_id'] = str(uuid4())

        print('-----------------------')
        print('-----------------------')
        print(request.data)
        print('-----------------------')
        print('-----------------------')

        if serializer.is_valid():
            serializer.save()


            SendEmail(
                send_to=email,
                subject='You are not invited cause youre not a spider',
                html='<p>Like the title said, youre not a spider, so youve not been inivited</p>'
            )


            return Response(
                {
                    'message':'success'
                })




        else:
            return Response(
                {
                    'error': True,
                    'message': 'Serializer is not valid',
                    'message_error' : serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)

        

        tenant_id = int(request.data['tenant_id'])
        
        try:
            tenant = Tenants.objects.get(id=tenant_id)
        except:
            return Response(
                {
                    'error': True,
                    'message': 'Tenant id provided does not exist'
                })
            
        
        serializer = TenantSerializer(tenant)


        
        return Response(serializer.data)
        
        print('----------------------------------')
        print('----------------------------------')
        
        print(request.data)
        
        SendEmail(
            send_to='andresruse18@gmail.com',
            subject='watson',
            html='<p>Success</p>'
        )
        
        
        print('----------------------------------')
        print('----------------------------------')
        
        return Response({'success':True})
        
    
    
