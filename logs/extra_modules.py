from django.utils import timezone
from .serializers import LogSerializer


def register_log(made_by:int, action:int, client_id:int, date_made:timezone, previous_data:dict=None, 
                 new_data:dict=None, tenant_id:int=None, unit_id:int=None, property_id:int=None):
    
    """Register the action the user made in the table of logs
    
    ACTION LOG MUST BE ONE OF THESE 
    
        1: CREATE
        2: EDIT
        3: DELETE
    """

    ACTION_LOG = {
        1: 'CREATE',
        2: 'EDIT',
        3: 'DELETE'
    }
    
    assert action in ACTION_LOG.keys(), 'action parameter must be 1:CREATE, 2:EDIT or 3:DELETE'

    log_data = {
                'client': client_id,
                'made_by': made_by,
                'action': ACTION_LOG[action],
                'date_made': date_made,
            }
    
    
    if previous_data:
        log_data['previous_data'] = previous_data
    
    if new_data:
        log_data['new_data'] = new_data
        
    is_deleted_data = ''
    if ACTION_LOG == 3:
        is_deleted_data = 'deleted_'
        
    if tenant_id:
        log_data[f'{is_deleted_data}tenant'] = tenant_id
        
    elif unit_id:
        log_data[f'{is_deleted_data}unit'] = unit_id
    
    elif property_id:
        log_data[f'{is_deleted_data}property'] = property_id
            
    log_serializer = LogSerializer(data=log_data)

    if log_serializer.is_valid():
        log_serializer.save()

    else:
        print('------------------------')
        print('- log serializer error -')
        print(log_serializer)
        print('------------------------')
        print('------------------------')