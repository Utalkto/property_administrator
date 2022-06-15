from django.db import models

from register.models import CustomUser, OrganizationClient
from properties.models import Unit, Property, Tenants
from tickets.models import Suppliers


class Log(models.Model):
    
    class Actions(models.TextChoices):
        CREATE = "CREATE"
        EDIT = "EDIT"
        DELETE = "DELETE"
    
    # foreignkeys 

    client = models.ForeignKey(OrganizationClient, null=False, blank=False, on_delete=models.CASCADE)
    made_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.PROTECT)
    
    unit = models.ForeignKey(Unit, null=True, blank=True, default=None, on_delete=models.PROTECT)
    property = models.ForeignKey(Property, null=True, blank=True, default=None, on_delete=models.PROTECT)
    tenant = models.ForeignKey(Tenants, null=True, blank=True, default=None, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Suppliers, null=True, blank=True, default=None, on_delete=models.PROTECT)
    
    deleted_unit = models.IntegerField(null=True, blank=True, default=None)
    deleted_property = models.IntegerField(null=True, blank=True, default=None)
    deleted_tenant = models.IntegerField(null=True, blank=True, default=None)
    deleted_supplier = models.IntegerField(null=True, blank=True, default=None)
    
    # Fields
    # ---------------------------------------------------
    
    action = models.CharField(max_length=120, choices=Actions.choices)
    date_made = models.DateTimeField()
    
    previous_data = models.JSONField(default=dict)
    new_data = models.JSONField(default=dict)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.action}'