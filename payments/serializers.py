from rest_framework import serializers
from .models import UnitPayments

from properties.serializers import UnitsSerializerProperty, TenantsNameSerializer

from .models import Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class RentPaymentGetSerializer(serializers.ModelSerializer):
    
    unit = UnitsSerializerProperty()
    tenant = TenantsNameSerializer()
    status = StatusSerializer()

    class Meta:
        model = UnitPayments
        fields = '__all__'
        

class RentPaymentsPostSerailizer(serializers.ModelSerializer):
    class Meta:
        model = UnitPayments
        fields = '__all__'