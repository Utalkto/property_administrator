from django.urls import path

from .views import home

urlpatterns = [
    
    path('', home)
    
    # path('properties',PropertiesViewSet.as_view()),
    # path('properties/<int:id>',PropertiesViewSet.as_view()),
    
    # path('units',UnitsViewSet.as_view()),
    # path('units/<int:id>',UnitsViewSet.as_view()),
    # path('unit/vacant/<int:unit_id>', vacantUnit),
    # path('set-unit-as-rented/<int:candidate_id>', set_unit_rented),
    
    # path('tenants/<int:id>',TenantViewSet.as_view()),
    # path('tenants',TenantViewSet.as_view()),

  
]