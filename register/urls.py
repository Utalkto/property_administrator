from django.urls import  path
from register.views import RecoverPasswordAPI, get_role, CreateUserView, check_if_invited

urlpatterns = [
    
    path('get-role/', get_role),
    path('create-user/', CreateUserView.as_view()),
    path('check_if_invited/<str:link>', check_if_invited),
    path('recover-password/', RecoverPasswordAPI.as_view()),

]

