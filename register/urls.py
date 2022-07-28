from django.urls import  path
from register.views import (RecoverPasswordAPI, get_role, CreateUserView, check_if_invited, confirm_user_email)


urlpatterns = [
    
    path('get-role/', get_role),
    path('create-user/', CreateUserView.as_view()),
    path('check_if_invited/<str:link>', check_if_invited),
    path('recover-password/', RecoverPasswordAPI.as_view()),
    path('confirm-user-email/', confirm_user_email),
    path('invation-link/', confirm_user_email),

]

