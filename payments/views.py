# django 

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView


from .models import UnitPayments
from .serializers import RentPaymentSerializer

# @api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
# def save_payments(request, unit_id):
#     pass


class RentPaymentApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    

    def get(self, request):

        serializer = RentPaymentSerializer(UnitPayments.objects.all(), many=True)
        
        return Response(serializer.data)
    