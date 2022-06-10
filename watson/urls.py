# django

from django.urls import path
from .views import WatsonApi, competition, trivia


urlpatterns = [
    
    path('watson_info/', WatsonApi.as_view()),
    path('competition/', competition),
    path('trivia/', trivia),
]