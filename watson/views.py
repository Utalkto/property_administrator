from rest_framework.views import APIView
from rest_framework.response import Response

from app_modules.send_email import SendEmail
from properties.models import Tenants
from properties.serializers import TenantSerializer
from .serializers import OrderSerializer

from rest_framework import status
from app_modules.send_email import SendEmail

from .models import Order, UserEmail, MessageToWatson

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


names = ['Tamaño', 'Masa', 'Ingredientes extras', 'Bebida', 'Helado']

{"detail0": "Pequeña",
 "detail1": "Gruesa", 
 "detail2": "Extra de vegetales", 
 "detail3": "Jugo de limón", 
 "detail4": "Mora"}


class WatsonApi(APIView):

    def post(self, request):

        if request.data.get('order_code'):
            try:
                order = Order.objects.get(order_code=request.data.get('order_code'))
            except Order.DoesNotExist :
                return Response({'error': 'code does not exist'})

            serializer = OrderSerializer(order)
            return Response(serializer.data)

        n = 0
        order = f'<p> Producto: {request.data["product"]} <p/>'
        details = dict()
        while True:
            current_key = f'detail{n}'
            if request.data.get(current_key) is None:
                break
            details[current_key] = request.data[current_key]
            order += f'<p> {names[n]} : {request.data[current_key]} </p>'
            n += 1

        
        code = random_with_N_digits(6)
        
        request.data['details'] = details
        serializer = OrderSerializer(data=request.data)
        email = request.data['email']

        request.data['order_code'] = code

        message = MessageToWatson(id=1).message

        if serializer.is_valid():
            serializer.save()
            
            from_email = 'support@utalkto.com'
            password = 'Support2022..'

            from_email = 'support@utalkto.com'
            password = 'Support2022..'

            # email to the client 
            SendEmail(
                send_to=email,
                subject='Confirmación de pedido. Pizzeria La Nona',
                html=f'<p>{message}</p> Su codigo de pedido es {code}</p> {order} <p> Tendra su pedido en 15 minutos. ¡Gracias por preferirnos!</p>',
                from_email=from_email,
                password=password
                
            )

            # email to the owner
            SendEmail(
                send_to=UserEmail.objects.get(id=1).email,
                subject='Nuevo pedido',
                html=f'<p>Se ha recibido un nuevo pedido bajo el codigo: {code}</p> {order}',
                from_email=from_email,
                password=password
            )


            return Response(
                {
                    'order_code': code,
                })

        else:

            print('-----------------------')
            print(serializer.errors)
            print('-----------------------')

            return Response(
                {
                    'error': True,
                    'message': 'Serializer is not valid',
                    'message_error' : serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)


        
        # taking the keys of the order to put it in the order

        # order += f'<p> Producto: {request.data["product"]} </p>'
        # order += f'<p> Masa: {request.data["dough"]} </p>'
        # order += f'<p> Ingrediente extra: {request.data["extra_toppingss"]} </p>'
        # order += f'<p> Bebida: {request.data["drink"]} </p>'
        # order += f'<p> Helado: {request.data["ice_cream"]} </p>'


        # for key in request.data:
        #     if key == 'email':
        #         continue

        #     d = request.data[key]
        #     spa_key = spanish[key]

        #     order += f'<p> {spa_key}: {d} </p>'
        

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
        
    
    
