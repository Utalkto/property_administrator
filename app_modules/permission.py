from register.models import CustomUser


def user_has_access(user:CustomUser, organization_id:int=None, client_id:int=None) -> bool:
    
    # checking if the user has access to the organization
    if organization_id:
        if user.organization.id != organization_id:
            return False
    
    # checking if the user has access to the clients
    if client_id:
        if client_id not in user.clients_access.keys():
            return False
    
    return True


def get_propeties_with_access(user:CustomUser) -> list[int]:
    properties = list()
    
    for key in user.clients_access.keys():
        properties += user.clients_access[key]['properties']
        
    
    return properties
    