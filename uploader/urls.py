from django.urls import  path

from .views import (UploadAPI)

urlpatterns = [
    path('<int:client_id>', UploadAPI.as_view())
]
    