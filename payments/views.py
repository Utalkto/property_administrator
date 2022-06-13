# django 

from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from book_keeping.models import PaymentRent
from properties.models import Units


from .models import UnitMonthlyPayments, UnitPayments
from .serializers import RentPaymentsPostSerailizer, RentPaymentGetSerializer, UnitMonthlyPaymentsGetSerializer

# @api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def save_payments(request, unit_id):
#     pass


class RentPaymentApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    

    def get(self, request):
        
        serializer = RentPaymentGetSerializer(UnitPayments.objects.filter(unit__property_manager=request.user.id), many=True)
        
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
        
        payment = UnitPayments.objects.get(id=payment_id)
        
        serializer = RentPaymentsPostSerailizer(instance=payment, data=request.data)
        
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
            UnitPayments.objects.get(id=int(payment_id)).delete()
        except:
            return Response(
                {
                    'error' : True,
                    'message_error' : 'There is no UnitPayments object with that id'
                }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
                'success': True,
                'message' : 'Deleted',
            }) 
    
    
class MonthlyPaymnetsApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request, client_id):
        pass
    
    def post(self, request, client_id):
        
        if request.GET.get('create_payments'):
            
            try:
                month = request.GET['month']
            except:
                return Response({
                    'message': 'when creating a new set of payments the month for that payment must be specified'
                    })
            
            units = Units.objects.filter(client=client_id)
            
            for unit in units:
                new_monthly_payment = UnitMonthlyPayments(
                    unit=unit,
                    month=month,
                    amount_to_pay=unit.rent,
                    pay_on_time=True,
                )
                
                unit.debt += unit.rent
                unit.save()
                new_monthly_payment.save()
            
            payments_serializer = UnitMonthlyPaymentsGetSerializer(UnitMonthlyPayments.objects.filter(month=month))
                
            return Response({
                payments_serializer.data
            })
                
            
            
            
            
            # unit = models.ForeignKey(Units, null=False, blank=False, on_delete=models.CASCADE)
            # # ------------------------------------------------
            # # fields 
            
            # month = models.CharField(max_length=120)
            # amount_to_pay = models.DecimalField(decimal_places=2, max_digits=10)
            # pay_on_time = models.BooleanField()
                
            
                
                
            
            