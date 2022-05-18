from django.urls import  path

from .views import CommunicationsAPI, communication_feed

urlpatterns = [
    
    path('feed/', communication_feed, name='communication_feed'),
    
    
    # API PART -------------------------------------
    
    path('send-message/', CommunicationsAPI.as_view()),
  

]