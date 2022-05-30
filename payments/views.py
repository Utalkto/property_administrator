# django 

from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from book_keeping.models import PaymentRent


from .models import UnitPayments
from .serializers import RentPaymentsPostSerailizer, RentPaymentGetSerializer

# @api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def save_payments(request, unit_id):
#     pass


class RentPaymentApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    

    def get(self, request):

        serializer = RentPaymentGetSerializer(UnitPayments.objects.all(), many=True)
        
        return Response(serializer.data)
    
    
    def post(self, request):
        
        serializer = RentPaymentsPostSerailizer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response({
                'error': True,
                'message' : 'Serializer is not valid',
                'error_message' : serializer.errors,
            })
        
    
    def put(self, request, payment_id):
        
        payment = PaymentRent.objects.get(id=payment_id)
        
        serializer = RentPaymentSerializer(instance=payment, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response({
                'error': True,
                'message' : 'Serializer is not valid',
                'error_message' : serializer.errors,
            })
        
        
    def delete(self, request, payment_id):
        
        try:
            PaymentRent.objects.get(id=int(payment_id)).delete()
        except:
            return Response(
                {
                    'error' : True,
                    'message_error' : 'There is no PaymentRent object with that id'
                }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
                'success': True,
                'message' : 'Deleted',
            }) 
    