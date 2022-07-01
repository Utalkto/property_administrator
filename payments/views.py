# django 
import datetime

from rest_framework import status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from properties.models import Unit
from django.utils import timezone


from .models import CurrentPaymentDate, UnitMonthlyPayments, UnitPayments
from .serializers import (RentPaymentsPostSerailizer, RentPaymentGetSerializer, 
                          UnitMonthlyPaymentsGetSerializer, UnitMonthlyPaymentsPostSerializer)

from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q

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
    
    
class MonthlyPaymentsApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    @swagger_auto_schema(
    responses={200: UnitMonthlyPaymentsPostSerializer()})
    def get(self, request, client_id):
        
        
        """MonthlyPaymentsApi GET

            parameters:
                client_id <int> (required) = The id of the client the sets of units are going to be returned
                
                from_date <int><query_parameter> (optional) = From the date it will take the registers, month and year included 
                
                to_date <int><query_parameter> (optional) = From the date it will take the registers, month and year not included 
        
        Returns:
            _type_: _description_
        """
        
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        
        if from_date is None:
            from_date = timezone.now()
        else:
            from_date = datetime.datetime.strptime(from_date, '%Y-%m')

        
        if to_date is None:
            to_date = 'all'
        else:
            try:
                to_date = datetime.datetime.strptime(to_date, '%Y-%m')
            except ValueError:
                return Response({
                    'error': f'Invalid format, the expected format is %Y-%m'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        response = dict()
        
        if request.GET.get('unit_id'):
            if to_date == 'all':
            
                payments = UnitMonthlyPayments.objects.filter(unit=int(request.GET['unit_id'])).filter(
                    Q(month__gte=from_date.strftime('%m')) | Q(year__gte=from_date.strftime('%Y')))
                  
            else:     
                payments = UnitMonthlyPayments.objects.filter(unit=int(request.GET['unit_id'])).filter(
                    Q(month__gte=int(from_date.strftime('%m'))) | Q(year__gte=int(from_date.strftime('%Y')))).filter(
                    Q(month__lt=int(to_date.strftime('%m'))) | Q(year__lt=int(to_date.strftime('%Y'))))
        else:
            if to_date == 'all':
            
                payments = UnitMonthlyPayments.objects.filter(unit__property__client=client_id).filter(
                    Q(month__gte=from_date.strftime('%m')) | Q(year__gte=from_date.strftime('%Y')))
                  
            else:     
                payments = UnitMonthlyPayments.objects.filter(unit__property__client=client_id).filter(
                    Q(month__gte=int(from_date.strftime('%m'))) | Q(year__gte=int(from_date.strftime('%Y')))).filter(
                    Q(month__lt=int(to_date.strftime('%m'))) | Q(year__lt=int(to_date.strftime('%Y'))))
            

        # if request.GET.get('incompleted_payments') is not None:
        completed_payments = payments.filter(debt=0).count()
        
        response['incompleted_payments'] = payments.count() - completed_payments
        response['completed_payments'] = completed_payments
        
        
        if request.GET.get('view_all'):
            serializer = UnitMonthlyPaymentsGetSerializer(payments, many=True)
            response['payments'] = serializer.data
            
            
        return Response(response)
            
        
    @swagger_auto_schema(
    responses={200: UnitMonthlyPaymentsPostSerializer()})
    def post(self, request, client_id):
        
        """MonthlyPaymnetsApi POST
        
        This post is to create a new set payments, it can be created for all of the unist that a client has
        or just to one client if the unit_id parameter is provided
        
        parameters:
            client_id <int> (required) = The id of the client the sets of units are going to be created
            
            objective_month <int><query_parameter> (required) = The objective month the set of payments will reach, if any month
            in between of the current month in db and the objective month is not create then they will be created
            
            objective_year <int><query_parameter> (required) = The objective year the set of payments will reach, if any year
            in between of the current year in db and the objective year is not create then they will be created
            
            unit_id <int><query_parameter> (optional) = if the unit id is given then the sets of payments are only going to be 
            create for that specific unit

        Returns:
            JSON: the last set of payments created 
        """
        
        try:
            objective_month = int(request.data.get('objective_month'))
            objective_year = int(request.data.get('objective_year'))
        except:
            return Response({
                'message': 'when creating a new set of payments the month for that payment must be specified'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        
        unit_id = request.data.get('unit_id')
        
        if unit_id is None:
            units = Unit.objects.all()
        elif unit_id is not None:
            units = [Unit.objects.get(id=int(unit_id))]

        
        last_payment_record = UnitMonthlyPayments.objects.last()
        current_date_in_db = CurrentPaymentDate.objects.last()
        if last_payment_record is None:
            current_month_in_db = int((timezone.now() - timezone.timedelta(weeks=5)).strftime('%m'))
            current_year_in_db = int(timezone.now().strftime('%Y'))
        else:
            current_month_in_db = current_date_in_db.month
            current_year_in_db = current_date_in_db.year
            
        records_creted = 0
        records_already_in_db = 0
        
        while objective_month != current_month_in_db or current_year_in_db != objective_year:
            
            month_to_put = current_month_in_db + 1
            
            if month_to_put > 12:
                month_to_put = 1
                current_year_in_db += 1
            
            year_to_put = current_year_in_db
            for unit in units:        
                if not UnitMonthlyPayments.objects.filter(unit=unit.id, month=month_to_put, year=year_to_put):
                    new_monthly_payment = UnitMonthlyPayments(
                        unit=unit,
                        month=month_to_put,
                        year=year_to_put,
                        debt=unit.rent,
                        paid_on_time=True,
                    )
                    
                    unit.debt += unit.rent
                    unit.save()
                    new_monthly_payment.save()
                    
                    records_creted += 1
                else:
                    records_already_in_db += 1
                
            current_month_in_db += 1
            
            if current_month_in_db > 12:
                current_month_in_db = 1
                
        if client_id is None:
            current_date_in_db.month = current_month_in_db
            current_date_in_db.year = current_year_in_db
            current_date_in_db.save()
        
        
        payments_serializer = UnitMonthlyPaymentsGetSerializer(
            UnitMonthlyPayments.objects.filter(month=objective_month), 
            many=True)

        try:
            total_units = units.count()
        except:
            total_units = 1
        
        return Response(
            {
                'payments': payments_serializer.data,
                'total_units': total_units,
                'record_created': records_creted,
                'records_already_in_db': records_already_in_db
                    
            })
        
        
    @swagger_auto_schema(
    responses={200: UnitMonthlyPaymentsPostSerializer()})
    def put(self, request, client_id):
        
        """MonthlyPaymnetsApi PUT
        
        parameters:
            client_id <int> (required) = The id of the client the payment belongs to 
            
            payment_id <int><query_parameter> (required) = the id of Jesus' elephant

        Returns:
            JSON: The information with the update payment object
        """
        
        try:
            payment_id = int(request.GET['payment_id'])
        except ValueError:
            return Response({'error': f'ValueError: payment_id must be int not {type(payment_id)}'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': f'KeyError: client_id must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        payment = UnitMonthlyPayments.objects.get(id=payment_id)
        
        serializer = UnitMonthlyPaymentsPostSerializer(instance=payment, data=request.data)
        
        if serializer.is_valid():
            return Response(serializer.data)
        
        else:
            return Response(
                {
                    'message_error': 'serializer is not valid',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
            
            
        
            
                
                
            
            