from django.urls import  path

from .views import ChatAPI, ChatMessageAPI, WritingInConversationAPI

urlpatterns = [
    
    path('chat/', ChatAPI.as_view()),
    path('check-if-writing/<int:conversation_id>', WritingInConversationAPI.as_view()),
    path('message/<int:conversation_id>', ChatMessageAPI.as_view())
    
]