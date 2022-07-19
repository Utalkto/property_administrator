from rest_framework import serializers, fields
from .extra_modules import TABLES

class UploaderQuerySerializer(serializers.Serializer):
    
    table = fields.ChoiceField(required=True, choices=list(TABLES.keys()))
    