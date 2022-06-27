from django.urls import  path

from .views import CommunicationsAPI, communication_feed, messages_details, twilio_in_bound

urlpatterns = [
    
    path('feed/<str:token>', communication_feed, name='communication_feed'),
    path('messages-details/<int:contact_id>/<str:user_type>/<str:token>', messages_details, name='messages_details' ),
    path('twilio-in-bound', twilio_in_bound),
    
    # API PART -------------------------------------
    
    path('messages/<int:client_id>', CommunicationsAPI.as_view()),

]