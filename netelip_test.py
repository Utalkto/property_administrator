"""

API FOR SMS: https://apidoc.netelip.com/v1/sms/?python#enviar-un-sms


import requests

url = 'https://api.netelip.com/v1/sms/api.php'
data = {
    'token'      : '69cizi7zc2394b9f84e97e78b8913d0ie1z2i6b58iec943fbz478z13c00d59cz',
    'from'       : 'anonymous',
    'destination': '0034666554433',
    'message'    : 'Esto es un mensaje de prueba'
}

response = requests.post(url=url, data=data)

if response:
    if response.status_code == 200:
        print('Mensaje enviado con exito')
    else:
        print('Error')
else:
    # Manejar error de conexión


"""

import requests

TOKEN = 'aefd105dd51348c31ddce12ddb04b5658f1ddb1980d47e6ca56b48b49c264d09'
NUMBER = '+15873300597'
DESTINATION = '+18642522485'

SEND_MESSAGE_URL = 'https://api.netelip.com/v1/sms/api.php'


data = {
    'token'      : TOKEN,
    'from'       : NUMBER,
    'destination': DESTINATION,
    'message'    : 'Testing this message'
}

response = requests.post(url=SEND_MESSAGE_URL, data=data)


if response.status_code == 200:
    print('Mensaje enviado con exito')
else:
    print('Error')
    print(response)

    