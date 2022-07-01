from rest_framework import serializers, fields

class PropertyAPIQuerySerializer(serializers.Serializer):
    property_id = fields.IntegerField(allow_null=True, default=None)