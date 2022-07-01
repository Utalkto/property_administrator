from django.urls import path

from .views import ToDoListAPI

urlpatterns = [
    path('todolist/<int:list_id>', ToDoListAPI.as_view())
]