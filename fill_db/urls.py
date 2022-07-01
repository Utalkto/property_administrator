from django.urls import path, include, re_path
from .views import fill_data_base


urlpatterns = [
    
    path('', fill_data_base, name='fill_data_base')
]