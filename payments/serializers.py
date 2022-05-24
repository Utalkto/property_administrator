from rest_framework import serializers
from .models import UnitPayments


class RentPaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitPayments
        fields = '__all__'
