def convert_to_bool(value):
    if type(value) == str:
        value = value.upper()
    
    if value in ['FALSE', 0, None]:
        return False
    
    return True