from rest_framework.views import APIView
from rest_framework.response import Response

from app_modules.send_email import SendEmail


class WatsonApi(APIView):



    def get(self, request):

        return Response({'success':True})

        
    
    def post(self, request):
        
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
        
    
    
