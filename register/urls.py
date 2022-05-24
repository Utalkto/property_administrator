from django.urls import  path
from register import  views

urlpatterns = [
    
    # path('<str:token>',views.DashboardViewSet.as_view()),
    path('get-role/',views.get_role),
    # path('example/',views.example_view),
  
]