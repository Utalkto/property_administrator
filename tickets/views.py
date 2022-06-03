# python 

import datetime

# django

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import status

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, authentication, permissions

# models 

from .models import SupplierWorkArea, Ticket, TicketPayment, TicketPriority, TicketType, MaintanenceType, MaintanenceIssueType, MaintanenceSubIssueType, MaintanenceIssueDescription, TicketAction, TicketSteps, Suppliers

from .serializers import SupplierGetSerializer, SupplierPostSerializer, TicketAppoinmentSerializer, TicketSerializer, TicketTypeSerializer, TicketPrioritySerializer, TicketCommentSerializer, WorkAreaSerializer

# properties
from properties.models import Properties, Tenants, Units
from properties.serializers import UnitsSerializer, TenantSerializer

from app_modules.decorators import check_login

# Create your views here.

# other functions
# -------------------------------------------------------------------------------------
def update_ticket_status(ticket:Ticket, to_status:int=None):
    
    if to_status is not None:
        ticket.ticket_status = TicketSteps.objects.get(id=to_status)
    
    else:
        ticket.ticket_status = TicketSteps.objects.get(id=ticket.ticket_status.id + 1)
        
    ticket.last_date_ticket_change = datetime.datetime.now()
    ticket.save()
    

# views 
# -------------------------------------------------------------------------------------
@check_login
def home(request, token):
    
    user_id = Token.objects.get(key=token).user.id
    
    all_tickets_open = Ticket.objects.filter(date_closed__isnull=True, owner=user_id)
    
    tickets_priority_low = Ticket.objects.filter(priority=3, date_closed__isnull=True, owner=user_id)
    tickets_priority_normal = Ticket.objects.filter(priority=2, date_closed__isnull=True, owner=user_id)
    tickets_priority_emergency = Ticket.objects.filter(priority=1, date_closed__isnull=True, owner=user_id)
    
    tickets_open = [ 
            { 'string':  'Priority Emergency', 'tickets': tickets_priority_emergency},
            { 'string':  'Priority Normal', 'tickets': tickets_priority_normal},
            { 'string':  'Priority Low', 'tickets': tickets_priority_low }] 
            
    maintenance_tickets = Ticket.objects.filter(ticket_type=1, date_closed__isnull=True).count()
    payment_tickets = Ticket.objects.filter(ticket_type=2, date_closed__isnull=True).count()
    general_info_tickets = Ticket.objects.filter(ticket_type=3, date_closed__isnull=True).count()
    ticket_statuses = TicketSteps.objects.all().order_by('id')
    
    return render(
        request, 
        'tickets/main_pages/dashboard-main.html', 
        {
            
            'tickets_open': tickets_open,
            
            'quantity_tickets_open': all_tickets_open.count(),
            'maintenance_tickets': maintenance_tickets,
            'payment_tickets': payment_tickets,
            'general_info_tickets': general_info_tickets,
            'ticket_statuses': ticket_statuses,
            'token' : token,
        })


def tickets_history(request, token):
    
    user_id = Token.objects.get(key=token).user.id
    ticket_statuses = TicketSteps.objects.all().order_by('id')
    maintenance_tickets = Ticket.objects.filter(ticket_type=1).count()
    
    
    tickets = Ticket.objects.filter(owner=user_id)
    
    total = len(tickets)
    
    print('---------------------------')
    print(tickets)
    print('---------------------------')
    
    
    return render(request, 
        'tickets/main_pages/tickets-history.html', 
        {
            'total_tickets': tickets,
            'total_count': total,
            'maintenance_tickets': maintenance_tickets,
            'ticket_statuses': ticket_statuses,
            'token': token,
        })
    

@check_login
def open_ticket(request, token):
    
    if request.method == 'POST':
        
        tenant_id = int(request.POST.get('tenant_id'))
        ticket_priority = int(request.POST.get('ticket_priority'))

        user_id = Token.objects.get(key=token).user.id
        
        data = {
            'created_by': tenant_id,
            'ticket_type': int(request.POST.get('ticket_type')),
            'stimated_time_for_solution_date': request.POST.get('sts_input'),
            'unit': Tenants.objects.get(id=tenant_id).unit.id,
            'date_opened' : datetime.datetime.now(),
            'priority': ticket_priority,
            'ticket_status': 1,
            'owner': user_id
        }
        
        serializer = TicketSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            return redirect('ticket_info', ticket_id=serializer.data['id'], token=token)
        
        else:
            return HttpResponse(serializer.errors)

    
    user_id = Token.objects.get(key=token).user.id

    return render(
        request, 
        'tickets/main_pages/create-ticket-with-search.html',
        {
            'tenants': Tenants.objects.filter(landlord=user_id),
            'ticket_types': TicketType.objects.all(),
            'ticket_priorities': TicketPriority.objects.all(),
            'token' : token,
        }
        ) 


##### DEPRECATED #####

@check_login
def create_ticket_main_info(request, token):
    
    next_stage = request.GET.get('next_stage')
    
    if next_stage == '1':
        
        units = UnitsSerializer(Units.objects.filter(property=int(request.GET.get('option_id'))), many=True)
        return JsonResponse({'options': units.data, 'stage_title': 'Select Unit', 'next_stage': 2} )
    
    elif next_stage == '2':
        
        tenants = TenantSerializer(Tenants.objects.filter(unit=int(request.GET.get('option_id'))), many=True)
        return JsonResponse( {'options': tenants.data, 'stage_title': 'Select Tenant', 'next_stage': 3} )
    
    
    elif next_stage == '3':
        
        tickets = TicketTypeSerializer(TicketType.objects.all(), many=True)
        return JsonResponse( {'options': tickets.data, 'stage_title': 'Select Type of issue', 'next_stage': 4} )
    
    elif next_stage == '4':
        priorities = TicketPrioritySerializer(TicketPriority.objects.all(), many=True)
        return JsonResponse( {'options':  priorities.data, 'next_stage': 5})
    
    
    elif next_stage == '5':
        
        ### start ticket creation ###
        tenant_id = int(request.GET.get('tenant_id'))
        ticket_priority = int(request.GET.get('option_id'))
        data = {
            'created_by': tenant_id,
            'ticket_type': int(request.GET.get('ticket_type')),
            'unit': Tenants.objects.get(id=tenant_id).unit.id,
            'date_opened' : datetime.datetime.now(),
            'priority': ticket_priority,
            'ticket_status': 1,
            'work_area' : 5, # TODO: change this here it can be dynamic
            # 'action_to_do': 1,
        }
        
        serializer = TicketSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            print(serializer.data)
            
            return JsonResponse( {'ticket_id': serializer.data['id']})
      
        else:
            print(serializer.errors)
            
            return JsonResponse(
                {
                    'message': 'serializer is not valid', 
                    'serializer_error': serializer.errors
                }, 
                
                status=status.HTTP_400_BAD_REQUEST
                )
    
    user_id = Token.objects.get(key=token).user.id
    properties = Properties.objects.filter(landlord=user_id)
    
    return render(
        request,
        'tickets/main_pages/create-ticket-dashboard.html',
        {
            'properties': properties, 
            'token': token
        })

##### ---------- #####

@check_login
def create_ticket_options(request,  token:str, ticket_type:int, ticket_id:int):
    
    if ticket_type == 1:
        fields = MaintanenceType.objects.all()
        
    form_fields = {}

    for i, _field in enumerate(list(fields)):
        form_fields[f'field{i}'] = {
            'id': _field.id,
            'string': _field.string_part
        }
        

    return render( 
        request,
        'tickets/main_pages/create-ticket-options.html', 
        {
            'form_fields': form_fields, 
            'branch_selected': ticket_type, 
            'ticket_id': ticket_id,
            'token' : token,
        })


@check_login
def ticket_info(request, token, ticket_id):
    
    ticket = Ticket.objects.get(id=int(ticket_id))
    ticket_statuses = TicketSteps.objects.filter(ticket_type=ticket.ticket_type.id).order_by('id')
    
    try:
        current_appoinment = list(ticket.ticketappoinment_set.filter(completed=False))[0]
    except:
        current_appoinment = None

        
    next_to_do = ticket_statuses[ticket.ticket_status.id]
    
    return render(
        request, 
        'tickets/main_pages/view-ticket-detail.html',
        {
            'ticket': ticket,
            'ticket_statuses': ticket_statuses,
            'next_to_do' : next_to_do,
            'comments' : Ticket.objects.get(id=ticket_id).ticketcomments_set.all().order_by('-date'),
            'token' : token,
            'current_appoinment': current_appoinment,
        }
        )


@check_login
def select_ticket_contractor(request, token, ticket_type, ticket_id):
    
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        contractors_ids = ticket.contractors_contacted
    except Ticket.DoesNotExist:
        return JsonResponse({"There is no ticket with that id"})
    
    
    if request.method == 'POST':
        
        data_for_serializer = dict()
        
        data_for_serializer['created_by'] = Token.objects.get(key=token).user.id
        data_for_serializer['ticket'] = ticket_id
        data_for_serializer['date'] = request.POST.get('appoinment_date')
        
        serializer = TicketAppoinmentSerializer(data=data_for_serializer)
        
        
        if serializer.is_valid():
            update_ticket_status(ticket=ticket)
            ticket.contractor = Suppliers.objects.get(id=int(request.POST.get('supplier_id')))
            ticket.save()
            
            serializer.save()
            
            return redirect('ticket_info', ticket_id=ticket.id, token=token)
        else:
            return JsonResponse({'there is no way is not valid': False, 'errors': serializer.errors })

    
    
    contractors_selected = list()
    for key in contractors_ids:
        contractors_selected.append(Suppliers.objects.get(id=int(contractors_ids[key])))

        
    return render (
        request,
        'tickets/main_pages/select-ticket-contractor.html',
        {
            'contractors': contractors_selected,
            'ticket': ticket,
            'token' : token,
        }
        )
    
    
def contact_ticket_contractor(request, token, ticket_type, ticket_id):
    """
    Function to contact a contractor 
    
    THE CONTRACTOR IS NOT CHOSEN HERE, to choose the contractor got to "select_ticket_contractor"

    Returns:
        _type_: _description_
    """
    
    
    ticket = Ticket.objects.get(id=int(ticket_id))
    
    if request.method == 'POST':
        
        # TODO: Send message (email or with tiwlio) to supplier
        
            json_model = ticket.contractors_contacted
            
            n = len(ticket.contractors_contacted.keys())
            json_model[f'contractor_{n}'] = request.POST.get('supplier_id')
            update_ticket_status(ticket=ticket) 
            ticket.save()
            
            return JsonResponse({'success': True})
            
    
    contractors_contacted = list()
    
    for contractor_id in ticket.contractors_contacted:
        contractors_contacted.append(ticket.contractors_contacted[contractor_id])
        
    work_areas = [ticket.issue_type.work_area.id]
    
    if ticket.sub_issue_type is not None:
        work_areas.append(ticket.sub_issue_type.work_area.id)
        
    if ticket.problem is not None:
        work_areas.append(ticket.problem.work_area.id)
    
    user_id = Token.objects.get(key=token).user.id
    
    recommended_contractors = Suppliers.objects.filter(work_area__in=work_areas, landlord=user_id).filter(~Q(id__in=contractors_contacted))
    other_contractors = Suppliers.objects.filter(landlord=user_id).filter(~Q(id__in=contractors_contacted))

    return render (
        request,
        'tickets/main_pages/contact-contractor.html',
        {
            'recommended_contractors': recommended_contractors,
            'other_contractors' : other_contractors,
            'ticket': ticket,
            'token' : token,
        }
        )
    

# JSON RESPONSES --------------------------------------------


def ticket_tree_stage_info(request): 
    
    branch_selected = int(request.POST.get('branch_selected'))
    stage_status = int(request.POST.get('next_stage'))
    option_selected = int(request.POST.get('option_selected'))
    current_tree_width = int(request.POST.get('current_tree_width'))
    
    ticket_id = int(request.POST.get('ticket_id'))
    ticket = Ticket.objects.get(id=ticket_id)
    
    # branch with id '1' is for maintanance
    if branch_selected == 1:
        
        # this will return the initial options <<maintanence_type>>
        if stage_status == 2:
            fields = MaintanenceIssueType.objects.filter(maintanence_type=option_selected)
            stage_title = 'Maintenance Issue'
            
        elif stage_status == 3:
            fields = MaintanenceSubIssueType.objects.filter(maintanence_issue_type=option_selected)
            stage_title = 'Sub Maintenance Issue'
            
            ticket.issue_type = MaintanenceIssueType.objects.get(id=option_selected)
            ticket.save()
            
        elif stage_status == 4:
            fields = MaintanenceIssueDescription.objects.filter(maintanence_issue_sub_type=option_selected)
            stage_title = 'Maintanence Issue Description'
            
            ticket.sub_issue_type = MaintanenceSubIssueType.objects.get(id=option_selected)
            ticket.save()
            
        elif stage_status == 5:
            
            
            ticket.ticket_status = TicketSteps.objects.get(id=2)
            ticket.action_to_do = TicketAction.objects.get(id=1)
            ticket.problem = MaintanenceIssueDescription.objects.get(id=option_selected)   
            
            ticket.save()
            
            return JsonResponse({'completed': True})
        
        
        if not len(fields):
            ticket_id = int(request.POST.get('ticket_id'))
            
            ticket = Ticket.objects.get(id=ticket_id)
            
            ticket.ticket_status = TicketSteps.objects.get(id=2)
            ticket.action_to_do = TicketAction.objects.get(id=1)
            
            if current_tree_width == 0:
            
                ticket.issue_type = MaintanenceIssueType.objects.get(id=option_selected)   
            
            elif current_tree_width == 1:
                
                ticket.sub_issue_type = MaintanenceSubIssueType.objects.get(id=option_selected)   
            
            ticket.save()
            
            return JsonResponse({'completed': True})
            
    
    form_fields = {}

    for i, _field in enumerate(list(fields)):
        form_fields[f'field{i}'] = {
            'id': _field.id,
            'string': _field.string_part
        }
        
    return JsonResponse({
        'form_fields': form_fields,
        'stage_title': stage_title,
        'current_stage' : stage_status + 1,
        'branch_selected' : branch_selected,
        'current_tree_width' : current_tree_width + 1,
        })


def solve_ticket_problem(request, token:str, ticket_id:int):
    
    ticket = Ticket.objects.get(id=int(ticket_id))
    
    update_ticket_status(ticket=ticket) 
    
    ticket.contractor_solution = request.POST.get('contractor_solution')
    ticket.solution_date = request.POST.get('solution_date')
    
    ticket.save()
    
    return redirect('ticket_info', ticket_id=ticket_id, token=token)


def register_payment_ticket(request, token:str, ticket_id:int):

    new_payment = TicketPayment(
        amount = request.POST.get('amount'),
        payment_date = request.POST.get('payment_date'),
        reference_code = request.POST.get('reference_code'),
        notes = request.POST.get('notes')
    )
    
    new_payment.save()
    ticket = Ticket.objects.get(id=int(ticket_id))
    
    update_ticket_status(ticket=ticket)
    ticket.payment = new_payment
    ticket.save()
    
    return redirect('ticket_info', ticket_id=ticket_id, token=token)
    
# API view


class TicketCommentApi(APIView):

    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    
    def get(self, request, ticket_id):
        
        ticket_comments =  Ticket.objects.get(id=ticket_id).ticketcomments_set.all()
        
        serializer = TicketCommentSerializer(ticket_comments, many=True)
        
        return JsonResponse(
            {'ticket_comments': serializer.data}, status=status.HTTP_200_OK)
        
    
    def post(self, request, ticket_id):
        
        
        request_data = request.data.copy()
        
        request_data['ticket'] = ticket_id
        request_data['date'] = datetime.datetime.now()
        request_data['made_by'] = request.user.id
        
        serializer = TicketCommentSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            
            
            return Response(
                {
                    'message': 'comment created successfully',
                    'comment': serializer.data,
                    'made_by': request.user.get_full_name()
                }, status=status.HTTP_201_CREATED)            
            
        else:
            return Response(
                {
                    'error': True,
                    'message': 'serializer is not valid',
                    'message_error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)          
           

class SuppliersApi(APIView):
    
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request, supplier_id:int):

        if supplier_id == 'all':
            serializer = SupplierGetSerializer(Suppliers.objects.filter(landlord=request.user.id), many=True)

        else:
            serializer = SupplierGetSerializer(Suppliers.objects.filter(id=int(supplier_id), landlord=request.user.id), many=True)

        return Response(serializer.data)
    
    
    def post(self, request):

        request.data['landlord'] = request.user.id
        serializer = SupplierPostSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
            
        else:
            return Response(
                    {
                    'error': True, 
                     'message': 'serializer is not valid', 
                     'serializer_error': serializer.errors
                    }, 
                    status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, supplier_id:int):
        
        request.data['landlord'] = request.user.id

        try:
            supplier = Suppliers.objects.get(id=supplier_id)
        except Suppliers.DoesNotExist:
            return Response(
                {
                    'error': True, 
                    'message ': 'Supplier with provided id does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
            
            
        serializer = SupplierPostSerializer(instance=supplier, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
    
            return Response(serializer.data)
        
        else: 
            return Response({
                'error': True,
                'message': 'serializer is not valid',
                'message_error': serializer.errors 
                })
        
        
    def delete(self, request, supplier_id:int):
        try:
            Suppliers.objects.get(id=supplier_id).delete()
        except Suppliers.DoesNotExist:
            return Response(
                {
                    'error': True, 
                    'message ': 'Supplier with provided id does not exist'
                }, 
                status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'success': True,
        })


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def close_ticket(request, ticket_id):
    
    ticket = Ticket.objects.get(id=int(ticket_id))
    ticket.date_closed = datetime.datetime.now()
    ticket.save()
    
    return Response({'success': True})
        

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def return_to_coordinate_visit(request, ticket_id):
    
    ticket=Ticket.objects.get(id=int(ticket_id))
    
    update_ticket_status(ticket=ticket, to_status=3)
    
    comment = f'Ticket got back to coordinate visit due to the fact that the problem was not solved by contractor {ticket.contractor.name}'
    
    if request.data.get('no_attendance'):
        appoinmnet = ticket.ticketappoinment_set.filter(completed=False)[0]
        
        appoinmnet.completed = True
        appoinmnet.supplier_attendance = False
        
        appoinmnet.save()
        
        
        comment = f'{ticket.contractor.name} did not attend the appoinment'
        
    
    data_for_comment = {
        'ticket' : ticket_id,
        'made_by' : request.user.id,
        'date': datetime.datetime.now(),
        'comment': comment
    }
    
    serializer = TicketCommentSerializer(data=data_for_comment)
    
    if serializer.is_valid():
        serializer.save()
    
    return Response({'success': True})
    
      
@api_view(['DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def delete_ticket(request, ticket_id):
    
    ticket = Ticket.objects.get(id=int(ticket_id))
    ticket.delete()
    
    return Response({'Ticket deleted': True})


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def total_tickets(request):
    
    total_tickets = Ticket.objects.filter(owner=request.user.id).count()
    opened_tickets = Ticket.objects.filter(date_closed__isnull=True, owner=request.user.id).count()
    
    
    return Response({
        'total_tickets' : total_tickets,
        'opened_tickets' : opened_tickets
    })
    

class WorkAreaApi(APIView):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializer = WorkAreaSerializer(SupplierWorkArea.objects.all(), many=True)
        return Response(serializer.data)



    