from rest_framework import serializers, fields


class TicketAPIQuerySerializer(serializers.Serializer):
    
    limit = fields.IntegerField(default=20, help_text="Indica la cantidad de tickets que ser quieren consultar, por defecto trae lost ultimos 20, set to null para que traiga todos")
    
    check_by_opened = fields.BooleanField(default=True, help_text="Devuelve los tickets que estan abiertos o cerrados, por defect trate los que estan abiertos, set to None para que traiga todos")
    check_by_priority = fields.IntegerField(default=None, help_text="Indica la prioridad de los tickets que se quieren consultar, por defecto trae todos")
    check_by_type = fields.IntegerField(default=None, help_text="Indica el type de los tickets que ser que se quieren consultar, por defecto trae todos")
    check_by_date_open = fields.DateField(default="1900-01-01", help_text="Indica la fecha a partir de la que quiere consultar, por defecto trae todos")
    check_by_status = fields.IntegerField(default=None, help_text="Indica el status de los tickets que se quieren consultar, por defecto trae todos")