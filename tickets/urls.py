from django.urls import path

from .views import home, create_ticket_main_info, create_ticket_options, ticket_info, ticket_tree_stage_info, select_ticket_contractor, open_ticket

urlpatterns = [
    path('', home, name='home'),
    
    # the next root will be deprecated
    path('create-ticket-main-info/', create_ticket_main_info, name='create_ticket_main_info'),
    # ----------------------------------------
    
    path('open-ticket/', open_ticket, name='open_ticket'),
    path('create-ticket-options/<int:ticket_type>/<int:ticket_id>', create_ticket_options, name='create_ticket_options'),
    
    path('stage-info/', ticket_tree_stage_info),
    
    path('ticket-info/<int:ticket_id>', ticket_info, name='ticket_info'),
    path('select-contractor/<int:ticket_type>/<int:ticket_id>', select_ticket_contractor, name='select_ticket_contractor')
    
    
    # path('properties',PropertiesViewSet.as_view()),
    # path('properties/<int:id>',PropertiesViewSet.as_view()),
    
    # path('units',UnitsViewSet.as_view()),
    # path('units/<int:id>',UnitsViewSet.as_view()),
    # path('unit/vacant/<int:unit_id>', vacantUnit),
    # path('set-unit-as-rented/<int:candidate_id>', set_unit_rented),
    
    # path('tenants/<int:id>',TenantViewSet.as_view()),
    # path('tenants',TenantViewSet.as_view()),

  
]