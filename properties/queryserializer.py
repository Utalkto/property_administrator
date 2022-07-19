from email.policy import default
from rest_framework import serializers, fields

class PropertyAPIQuerySerializer(serializers.Serializer):
    property_id = fields.CharField(allow_null=True, default=None)

class TenantAPIQuerySerializer(serializers.Serializer):
    tenant_id = fields.CharField(allow_null=True, default=None)

class UnitAPIQueryserializer(serializers.Serializer):
    unit_id = fields.CharField(allow_null=True, default=None)

