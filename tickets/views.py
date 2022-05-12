from django.http import JsonResponse
from django.shortcuts import render
from .models import TicketType, MaintanenceType, MaintanenceIssueType, MaintanenceSubIssueType, MaintanenceIssueDescription, TicketAction

# Create your views here.

def home(request):
    return render(request, 'tickets/main_pages/home.html', {'variable1': ['uno', 'dos', 'tres']})



def create_ticket(request):
    
    # ticket_type = TicketType.objects.all()
    
    maintenance_type = MaintanenceType.objects.all()
    
    form_fields = {}
    
    for i, _field in enumerate(maintenance_type):
        form_fields[f'field{i}'] = {
            'id': _field.id,
            'string': _field._string
        }
    
    return render(
        request,
        'tickets/main_pages/create-ticket.html',
        {
            'form_fields': form_fields,
            'branch_selected' : 1,
            
        })



def stage_info(request): 
    
    branch_selected = int(request.POST.get('branch_selected'))
    stage_status = int(request.POST.get('next_stage'))
    option_selected = int(request.POST.get('option_selected'))
    
    # branch with id '1' is for maintanance
    if branch_selected == 1:
        
        # this will return the initial options <<maintanence_type>>
        if stage_status == 1:
            fields = MaintanenceType.objects.all()
        
        elif stage_status == 2:
            fields = MaintanenceIssueType.objects.filter(maintanence_type=option_selected)
            stage_title = 'Maintanence Issue'
        
        elif stage_status == 3:
            fields = MaintanenceSubIssueType.objects.filter(maintanence_issue_type=option_selected)
            stage_title = 'Sub Maintanence Issue'
            
        elif stage_status == 4:
            fields = MaintanenceIssueDescription.objects.filter(maintanence_issue_sub_type=option_selected)
            stage_title = 'Maintanence Issue Description'
        
        elif stage_status == 5:
            fields = TicketAction.objects.filter(issue_description=option_selected)
            stage_title = 'Action to do'
            
    
    form_fields = {}

    for i, _field in enumerate(list(fields)):
        form_fields[f'field{i}'] = {
            'id': _field.id,
            'string': _field._string
        }
        
    return JsonResponse({
        'form_fields': form_fields,
        'stage_title': stage_title,
        'current_stage' : stage_status + 1,
        'branch_selected' : branch_selected
        })
