from django.urls import path

from .views import WorkAreaApi, tickets_history, home, SuppliersApi, delete_ticket, return_to_coordinate_visit, close_ticket, register_payment_ticket, solve_ticket_problem, select_ticket_contractor, create_ticket_main_info, create_ticket_options, ticket_info, ticket_tree_stage_info, contact_ticket_contractor, open_ticket, TicketCommentApi, total_tickets

urlpatterns = [
    path('home/<str:token>', home, name='home'),
    
    
    path('history/<str:token>', tickets_history, name='tickets_history'),
    
    # the next root will be deprecated
    path('create-ticket-main-info/<str:token>', create_ticket_main_info, name='create_ticket_main_info'),
    # ----------------------------------------
    
    path('open-ticket/<str:token>', open_ticket, name='open_ticket'),
    path('create-ticket-options/<str:token>/<int:ticket_type>/<int:ticket_id>', create_ticket_options, name='create_ticket_options'),
    
    path('stage-info/', ticket_tree_stage_info),
    
    path('ticket-info/<str:token>/<int:ticket_id>', ticket_info, name='ticket_info'),
    path('contact-contractor/<str:token>/<int:ticket_type>/<int:ticket_id>', contact_ticket_contractor, name='contact_ticket_contractor'),
    path('select-contractor/<str:token>/<int:ticket_type>/<int:ticket_id>', select_ticket_contractor, name='select_ticket_contractor'),
    
    # Json reponse only and redirect
    
    path('solve-problem/<str:token>/<int:ticket_id>', solve_ticket_problem),
    path('register-payment/<str:token>/<int:ticket_id>', register_payment_ticket),
    
    path('close-ticket/<int:ticket_id>', close_ticket),
    path('return-to-coordinate-visit/<int:ticket_id>', return_to_coordinate_visit),
    path('delete-ticket/<int:ticket_id>', delete_ticket),
    path('total-tickets/', total_tickets),

    # apis

    path('ticket-comment/<int:ticket_id>', TicketCommentApi.as_view()),
    path('suppliers/<str:supplier_id>', SuppliersApi.as_view()),
    path('work-areas/', WorkAreaApi.as_view() )
    
    
]