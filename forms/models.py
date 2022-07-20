from enum import Enum
import secrets

from django.db import models

from django.utils import timezone

from register.models import CustomUser, OrganizationClient
from properties.models import Unit


class Form(models.Model):

    # foreign fields
    
    client = models.ForeignKey(OrganizationClient, related_name='client', on_delete=models.CASCADE)    
    unit = models.ForeignKey(Unit, null=True, blank=True, default=None, related_name='unit', on_delete=models.CASCADE)
    
    # --------------------------------------------------
    # fields
    
    description = models.CharField(max_length=255, default='')
    
    form_fields = models.JSONField()
    
    link = models.CharField(max_length=255, default='__no_link__')
    
    name = models.CharField(max_length=255)
    number_of_views = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    # intern fields ----------------------------------------------------------------
    
    datetime_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(CustomUser, default=1, on_delete=models.PROTECT, related_name='created_by')
    
    last_time_edited = models.DateTimeField(null=True, default=None)
    last_edition_made_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT, 
                                             default=None, related_name='last_edition_made_by')
    
    
    def save(self, **kwargs):
        
        if self.link == '__no_link__':
            self.link = secrets.token_urlsafe(26)
        
        super().save(**kwargs)

    
# forms fields must be JSON that need to look like this 

# {
#     [
#         {
#             "type": "text",
#             "placeholer": "placeholder",
#             "label": "This is a test",
#             "size": "normal",
#             "color": "primary",
#             "icon": False,
#         }
#     ]
# }
       
    
    
    

    
    