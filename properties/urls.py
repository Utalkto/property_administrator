from django.urls import  path

from .views import PropertiesViewSet, TenantViewSet, UnitsViewSet, vacantUnit, set_unit_rented, data_to_create_property

urlpatterns = [
    
    path('properties',PropertiesViewSet.as_view()),
    path('properties/<int:property_id>',PropertiesViewSet.as_view()),
    
    path('units',UnitsViewSet.as_view()),
    path('units/<int:unit_id>',UnitsViewSet.as_view()),
    
    
    
    path('unit/vacant/<int:unit_id>', vacantUnit),
    path('set-unit-as-rented/<int:candidate_id>', set_unit_rented),
    
    path('tenants/<int:tenant_id>/<int:property_id>',TenantViewSet.as_view()),
    path('tenants',TenantViewSet.as_view()),
    
    path('info-to-create-property', data_to_create_property)
    

]