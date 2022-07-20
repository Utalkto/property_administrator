from rest_framework import serializers, fields


class FormQuerySerializer(serializers.Serializer):
    
    unit_id = fields.IntegerField(default=None)
    