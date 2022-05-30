from rest_framework.views import APIView
from rest_framework.response import Response

from app_modules.send_email import SendEmail
from properties.models import Tenants
from properties.serializers import TenantSerializer
from .serializers import ProductSerializer

from rest_framework import status
from app_modules.send_email import SendEmail

from .models import Product, UserEmail, MessageToWatson

from uuid import uuid4


from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

spanish = {
        'dough': 'Masa',
        'drink' : 'Bebida',
        'product' : 'Producto',
        'ice_cream': 'Helado',
        'extra_toppings': 'Ingredientes extra'
        }


class WatsonApi(APIView):

    {'dough': 'Delgada', 
    'drink': 'Coca Cola', 
    'email': 'acampos@utalkto.com', 
    'product': 'Napolitana', 
    'ice_cream': 'Fresas con crema', 
    'extra_toppings': 'Extra de queso', 
    'product_id': 'fe4962fe-5db7-46ab-8a17-33de31cb143e'}

    def post(self, request):

        if request.data.get('order_code'):
            try:
                order = Product.objects.get(order_code=request.data.get('order_code'))
            except Product.DoesNotExist :
                return Response({'error': 'code does not exist'})

            serializer = ProductSerializer(order)
            return Response(serializer.data)

        
        code = random_with_N_digits(6)
        serializer = ProductSerializer(data=request.data)
        email = request.data['email']

        order = str()

        # taking the keys of the order to put it in the order

        order += f'<p> Producto: {request.data["product"]} </p>'
        order += f'<p> Masa: {request.data["dough"]} </p>'
        order += f'<p> Ingrediente extra: {request.data["extra_toppingss"]} </p>'
        order += f'<p> Bebida: {request.data["drink"]} </p>'
        order += f'<p> Helado: {request.data["ice_cream"]} </p>'


        # for key in request.data:
        #     if key == 'email':
        #         continue

        #     d = request.data[key]
        #     spa_key = spanish[key]

        #     order += f'<p> {spa_key}: {d} </p>'

        request.data['product_id'] = str(uuid4())
        request.data['order_code'] = code

        message = MessageToWatson(id=1).message

        if serializer.is_valid():
            serializer.save()

            # email to the client 
            SendEmail(
                send_to=email,
                subject='Confirmación de pedido. Pizzeria La Nona',
                html=f'<p>{message}</p> su codigo de pedido es {code}</p> {order} <p> Tendra su pedido en 15 minutos. ¡Gracias por preferirnos!</p>'
            )

            # email to the owner
            SendEmail(
                send_to=UserEmail.objects.get(id=1).email,
                subject='Nuevo pedido',
                html=f'<p>Se ha recibido un nuevo pedido bajo el codigo: {code}</p> {order}'
            )


            return Response(
                {
                    'order_code': code,
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
        
    
    
