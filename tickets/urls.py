from django.urls import path

from .views import home, create_ticket_main_info, create_ticket_options, ticket_info, ticket_tree_stage_info

urlpatterns = [
    path('', home, name='home'),
    path('create-ticket-main-info/', create_ticket_main_info, name='create_ticket_main_info'),
    path('create-ticket-options/<int:ticket_type>/<int:tenant_id>', create_ticket_options, name='create_ticket_options'),
    
    path('stage-info/', ticket_tree_stage_info),
    
    path('ticket-info/<ticket_id>', ticket_info, name='ticket_info'),
    
    
    # path('properties',PropertiesViewSet.as_view()),
    # path('properties/<int:id>',PropertiesViewSet.as_view()),
    
    # path('units',UnitsViewSet.as_view()),
    # path('units/<int:id>',UnitsViewSet.as_view()),
    # path('unit/vacant/<int:unit_id>', vacantUnit),
    # path('set-unit-as-rented/<int:candidate_id>', set_unit_rented),
    
    # path('tenants/<int:id>',TenantViewSet.as_view()),
    # path('tenants',TenantViewSet.as_view()),

  
]