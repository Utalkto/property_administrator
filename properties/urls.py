from django.urls import  path

from .views import (PropertyAPI, TeamApi, TenantViewSet, UnitsAPI, 
                    vacantUnit, set_unit_rented, data_to_create_property)

urlpatterns = [
    
    path('properties/<int:client_id>',PropertyAPI.as_view()),
    
    path('units/<int:client_id>',UnitsAPI.as_view()),
    
    path('unit/vacant/<int:unit_id>', vacantUnit),
    path('set-unit-as-rented/<int:candidate_id>', set_unit_rented),
    
    path('tenants/<int:tenant_id>/<int:property_id>',TenantViewSet.as_view()),
    path('tenants',TenantViewSet.as_view()),
    
    path('info-to-create-property', data_to_create_property),
    
    path('team', TeamApi.as_view()),
    path('team/<str:team_id>', TeamApi.as_view()),
]