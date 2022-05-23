from django.urls import path

from .views import home, select_ticket_contractor, create_ticket_main_info, create_ticket_options, ticket_info, ticket_tree_stage_info, contact_ticket_contractor, open_ticket, TicketCommentApi

urlpatterns = [
    path('', home, name='home'),
    
    # the next root will be deprecated
    path('create-ticket-main-info/', create_ticket_main_info, name='create_ticket_main_info'),
    # ----------------------------------------
    
    path('open-ticket/', open_ticket, name='open_ticket'),
    path('create-ticket-options/<int:ticket_type>/<int:ticket_id>', create_ticket_options, name='create_ticket_options'),
    
    path('stage-info/', ticket_tree_stage_info),
    
    path('ticket-info/<int:ticket_id>', ticket_info, name='ticket_info'),
    path('contact-contractor/<int:ticket_type>/<int:ticket_id>', contact_ticket_contractor, name='contact_ticket_contractor'),
    path('select-contractor/<int:ticket_type>/<int:ticket_id>', select_ticket_contractor, name='select_ticket_contractor'),
    
    # Json reponse only 
    
    path('ticket-comment/<int:ticket_id>', TicketCommentApi.as_view()),
    
    
]