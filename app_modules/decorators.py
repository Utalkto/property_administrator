from rest_framework.authtoken.models import Token
from django.core.exceptions import PermissionDenied


def check_login(function):
    def wrap(request, *args, **kwargs):
        try:
            Token.objects.get(key=kwargs['token'])
        except:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return wrap