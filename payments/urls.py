from django.urls import path


from .views import RentPaymentApi

urlpatterns = [
    path('rent-payments/', RentPaymentApi.as_view())
]