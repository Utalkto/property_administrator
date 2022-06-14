from rest_framework.views import APIView
from rest_framework.response import Response

from app_modules.send_email import SendEmail
from properties.models import Properties, Tenants, Units
from properties.serializers import PropertiesSerializer, TenantSerializer, UnitsSerializerGet
from .serializers import OrderSerializer
from rest_framework import status

from rest_framework import status
from app_modules.send_email import SendEmail

from .models import Order, Subjects, UserEmail, MessageToWatson
from rest_framework.decorators import api_view, authentication_classes, permission_classes

import datetime

import inflect
p = inflect.engine()

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
            order += f'<p> {names[n]}: {request.data[current_key]} </p>'
            n += 1

        
        code = random_with_N_digits(6)
        
        request.data['details'] = details
        serializer = OrderSerializer(data=request.data)
        email = request.data['email']

        request.data['order_code'] = code

        message = MessageToWatson.objects.get(id=1).message
        subject = Subjects.objects.get(id=1).subject

        if serializer.is_valid():
            serializer.save()
            
            from_email = 'support@utalkto.com'
            password = 'Support2022..'

            from_email = 'support@utalkto.com'
            password = 'Support2022..'

            address = request.data['address']
            #price = request.data['price']

            print('message')
            print(message)

            message = str(message).replace('{code}', str(code)).replace('{order}', order).replace('{address}', str(address))

            print('-----------------------')
            print(message)
            print('-----------------------')

            # email to the client 
            SendEmail(
                send_to=email,
                subject=str(subject).replace('{code}', str(code)),
                html=message,
                from_email=from_email,
                password=password                  
            )
            
            # email to the owner
            SendEmail(
                send_to=UserEmail.objects.get(id=1).email,
                subject='Nuevo pedido',
                html=f'<p>Se ha recibido un nuevo pedido bajo el codigo: {code}</p> {order} <p>Dirección: {address}</p> <p>Precio: $10</p>',
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
        
    
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def competition(request):

    phone_number = request.data.get('phone_number')


    SendEmail(
        send_to='support@utalkto.com',
        subject='Nuevo ganador',
        html=f'<p>Hay un nuevo ganador.</p> <p>Número de teléfono: {phone_number}</p>'
    )

    return Response({'message': 'Success'})



import requests

TRIVIA_URL = 'http://178.18.250.142/vicidial/non_agent_api.php'

@api_view(['POST'])
def trivia(request):
    
    parameters = {
        'source':'test',
        'user':'carga_lead',
        'pass':'Ncrg4900',
        'function':'add_lead',
        'phone_number':request.data['phone_number'],
        'phone_code':1,
        'list_id':250,
        'dnc_check':'N',
        'campaign_dnc_check':'Y',
        'campaign_id':'in_sms',
        'first_name':request.data['first_name'],
        'last_name':request.data['last_name'],
        'address1':request.data['address'],
        'city':request.data['city'],
        'state':'VE',
        'add_to_hopper':'Y',
    }
    
    response = requests.request("POST", TRIVIA_URL, params=parameters)
    
    print('--------------------------------')
    print('--------------------------------')
    print(response.text)
    print('--------------------------------')
    print('--------------------------------')
    
    
    return Response({'message':'success'})


@api_view(['POST'])
def property_api(request):

    property_name = request.data['property_name']

    try:
        property_serializer = PropertiesSerializer(Properties.objects.get(name=property_name))
    
    except Properties.DoesNotExist:
        return Response({
            'message': f'property with name "{property_name}" does not exist in the data base'
            })
        
        
    unit_serializer = UnitsSerializerGet(Units.objects.filter(property=property_serializer.data['id']).first())

    unit_serializer = unit_serializer.data


    date_time_obj = datetime.datetime.strptime(unit_serializer['availability'], '%Y-%m-%d')

    availability_date = date_time_obj.strftime('%B')
    availability_date += " " + p.ordinal(date_time_obj.strftime('%d'))
    unit_serializer['availability'] = availability_date
    
    unit_serializer['limit_date'] = date_time_obj + datetime.timedelta(weeks=2)
    
    
    if unit_serializer['balcony']:
        unit_serializer['balcony'] = 'Yes, there is a private balcony.'
    else:
        unit_serializer['balcony'] = 'No, unfortunately there is no balcony.'
        
    if unit_serializer['video_tour']:
        unit_serializer['video_tour'] = "Yes, we can arrange a video tour! At the moment we don't have any video from the unit, but in a few days we can record a few and send them to you.You can request a viewing and fill our form so we can have your contact information."
    else:
        unit_serializer['video_tour'] = 'No, unfortunately there is no balcony.'
        
    if unit_serializer['private_unit']:
        unit_serializer['private_unit'] = 'The unit is completely private.'
    else:
        unit_serializer['private_unit'] = 'No, this unit is not private.'
        
    if unit_serializer['yard']:
        unit_serializer['yard'] = "Yes, the unit has a yard."
    else:
        unit_serializer['yard'] = "Unfortunately, there isn't a fenced yard"
        
    if unit_serializer['outdoor_storage']:
        unit_serializer['outdoor_storage'] = "Yes, the unit has an outdoor storage."
    else:
        unit_serializer['outdoor_storage'] = "Unfortunately, there isn't outdoor storage."

    
    if 'washer' in unit_serializer['servicesss'].keys() or 'dryer' in unit_serializer['servicesss'].keys():
        unit_serializer['washer_dryer'] = 'There is a washer and a dryer in the unit.'
    else:
        unit_serializer['washer_dryer'] = "Unfortunately, the unit does not have these appliances."
        
    if unit_serializer['basement_unit']:
        unit_serializer['basement_unit'] = 'Yes, the unit is a basement unit.'
    else:
        unit_serializer['basement_unit'] = "No, the unit is not a basement unit."
        
    if unit_serializer['people_above']:
        unit_serializer['people_above'] = 'Yes, there are people above the unit.'
    else:
        unit_serializer['people_above'] = "No, there aren't people above."
    
    if unit_serializer['unemployed_people']:
        unit_serializer['unemployed_people'] = 'Absolutely! We encourage everyone to go through the application process.'
    else:
        unit_serializer['unemployed_people'] = "No, we don't accept unemployed people in this unit."
        
    if unit_serializer['kids']:
        unit_serializer['kids'] = 'Absolutely, kids are allowed in the unit.'
    else:
        unit_serializer['kids'] = "No, kids aren't allowed in the unit."
        
    if unit_serializer['pet_friendly']:
        unit_serializer['pet_friendly'] = f'Yes, some pets are allowed.'
    else:
        unit_serializer['pet_friendly'] = "No, pets aren't allowed in the unit."

    
    d = {**property_serializer.data, **unit_serializer}

    return Response(d)