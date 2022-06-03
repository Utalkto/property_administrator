from django.urls import path
from .views import ExpensesApi, CategoriesApi

urlpatterns = [
    path('expenses', ExpensesApi.as_view()),
    path('expenses/<str:expenses_id>', ExpensesApi.as_view()),
    path('expenses-categories', CategoriesApi.as_view()),
]
