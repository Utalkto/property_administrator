from django.urls import path

from .views import CommentsAPI

urlpatterns = [
    path('comments/<int:client_id>', CommentsAPI.as_view())
]