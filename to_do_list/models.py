from django.db import models
from register.models import CustomUser


class ToDoList(models.Model):
    # ForeignKey 
    
    onwer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # --------------------------------------------------------
    # Fields 
    
    completed = models.BooleanField(default=False)
    text = models.TextField()
    
