from django.urls import path
from .views import LogAPI

urlpatterns = [
    path('logs/<int:organization_id>', LogAPI.as_view())
]