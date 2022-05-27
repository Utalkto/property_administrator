from django.urls import path
from .views import ExpensesApi

urlpatterns = [
    path('expenses', ExpensesApi.as_view()),
    path('expenses/<str:expenses_id>', ExpensesApi.as_view()),
]
