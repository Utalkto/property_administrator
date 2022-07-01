from django.db import models

from register.models import CustomUser, OrganizationClient

class Comment(models.Model):
    # Foreign keys 
    # -------------------------------------------------------
    
    client = models.ForeignKey(OrganizationClient, null=False, blank=False, on_delete=models.CASCADE)
    made_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
    
    # -------------------------------------------------------
    
    comment = models.TextField()
    date_made = models.DateTimeField()
    users_taged = models.JSONField(default=list)
    

class CommentAnswer(models.Model):
    # Foreign keys 
    # -------------------------------------------------------
    
    comment = models.ForeignKey(Comment, null=False, blank=False, on_delete=models.CASCADE)
    made_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE)
      
    # -------------------------------------------------------
    
    answer = models.TextField()
    date_made = models.DateTimeField()
    users_taged = models.JSONField(default=list)
    
    

