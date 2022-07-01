# django

from django.urls import path
from .views import WatsonApi, competition, open_dental, trivia, property_api


urlpatterns = [
    
    path('watson_info/', WatsonApi.as_view()),
    path('competition/', competition),
    path('trivia/', trivia),
    path('property/', property_api),
    path('open_dental/', open_dental)
]