from rest_framework import serializers

from .models import Log
from register.serializers import OrganizationClient, UserSerializer

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
        
        
class LogRelatedDataSerializer(serializers.ModelSerializer):
    client = OrganizationClient()
    made_by = UserSerializer()
    class Meta:
        model = Log
        fields = '__all__'

# unit = models.ForeignKey(Unit, null=True, blank=True, default=None, on_delete=models.PROTECT)
# property = models.ForeignKey(Property, null=True, blank=True, default=None, on_delete=models.PROTECT)
# tenant = models.ForeignKey(Tenants, null=True, blank=True, default=None, on_delete=models.PROTECT)
# supplier = models.ForeignKey(Suppliers, null=True, blank=True, default=None, on_delete=models.PROTECT)