# django

from django.urls import path
from .views import WatsonApi


urlpatterns = [
    
    path('watson_info/', WatsonApi.as_view())
]