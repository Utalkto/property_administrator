from django.urls import path, include, re_path

from .views import FormsAPI

urlpatterns = [
    
    path('forms/<int:client_id>/', FormsAPI.as_view()),
    
]