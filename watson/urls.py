# django

from django.urls import path
from .views import WatsonApi, competition


urlpatterns = [
    
    path('watson_info/', WatsonApi.as_view()),
    path('competition/', competition)
]