from django.db import models
from register.models import CustomUser


class ToDoList(models.Model):
    # ForeignKey 
    
    onwer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # --------------------------------------------------------
    # Fields 
    
    name = models.CharField(max_length=120, default='')
    

class Task(models.Model):
    
    to_do_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    
    completed = models.BooleanField(default=False)
    task = models.TextField()
    
