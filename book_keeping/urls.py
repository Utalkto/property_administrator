from django.urls import path
from .views import ExpensesApi, CategoriesApi, BankAccountApi

urlpatterns = [
    path('expenses', ExpensesApi.as_view()),
    path('expenses/<str:expenses_id>', ExpensesApi.as_view()),
    path('expenses-categories', CategoriesApi.as_view()),
    path('banks/<str:bank_account_id>', BankAccountApi.as_view())
]
