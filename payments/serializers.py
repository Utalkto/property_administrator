from rest_framework import serializers
from .models import UnitMonthlyPayments, UnitPayments

from properties.serializers import UnitRelatedFieldsSerializer, TenantRelatedFieldsSerializer

from .models import Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class RentPaymentGetSerializer(serializers.ModelSerializer):
    
    unit = UnitRelatedFieldsSerializer()
    tenant = TenantRelatedFieldsSerializer()
    status = StatusSerializer()

    class Meta:
        model = UnitPayments
        fields = '__all__'
        

class RentPaymentsPostSerailizer(serializers.ModelSerializer):
    class Meta:
        model = UnitPayments
        fields = '__all__'
        
        
class UnitMonthlyPaymentsGetSerializer(serializers.ModelSerializer):
    unit = UnitRelatedFieldsSerializer()
    class Meta:
        model = UnitMonthlyPayments
        fields = '__all__'


class UnitMonthlyPaymentsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitMonthlyPayments
        fields = '__all__'