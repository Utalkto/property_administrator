from django.urls import  path

from .views import ConversationsAPI, communication_feed, messages_details, netelip_message_view, twilio_in_bound_sms, get_latest_messages, twilio_in_bound_call

urlpatterns = [
    
    path('feed/<str:token>', communication_feed, name='communication_feed'),
    path('messages-details/<int:contact_id>/<str:user_type>/<str:token>', messages_details, name='messages_details' ),
    path('twilio-in-bound', twilio_in_bound_sms),
    
    # API PART -------------------------------------
    
    path('conversations/<int:client_id>', ConversationsAPI.as_view()),
    path('latest-messages/<int:client_id>', get_latest_messages),
    path('twilio-call-in-bound', twilio_in_bound_call),
    path('netelip-test/', netelip_message_view)

]