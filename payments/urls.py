from django.urls import path


from .views import RentPaymentApi, MonthlyPaymentsApi

urlpatterns = [
    path('rent-payments/', RentPaymentApi.as_view()),
    path('rent-payments/<int:payment_id>', RentPaymentApi.as_view()),
    path('monthly-payments/<int:client_id>', MonthlyPaymentsApi.as_view())
]