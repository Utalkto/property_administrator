from django.urls import  path

from .views import PropertiesViewSet, TenantViewSet, UnitsViewSet, vacantUnit

urlpatterns = [
    
    path('properties',PropertiesViewSet.as_view()),
    path('properties/<int:id>',PropertiesViewSet.as_view()),
    
    path('units',UnitsViewSet.as_view()),
    path('units/<int:id>',UnitsViewSet.as_view()),
    path('unit/vacant/<int:id>',vacantUnit),
    
    path('tenants/<int:id>',TenantViewSet.as_view()),
    path('tenants',TenantViewSet.as_view()),
  
]