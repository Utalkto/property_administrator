from django.db import models
from register.models import CustomUser, OrganizationClient


class NotificationType(models.Model):
    
    type = models.CharField(max_length=120)


class Notification(models.Model):

    client = models.ForeignKey(OrganizationClient, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, null=False, blank=False, on_delete=models.CASCADE)


    # fields --------------------------------------------

    created_date = models.DateTimeField()
    
    notification = models.TextField()
    
    sent_to_email = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    
    
