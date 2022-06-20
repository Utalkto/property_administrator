from django.contrib import admin
from .models import ToDoList, Task


admin.site.register(Task)
admin.site.register(ToDoList)
