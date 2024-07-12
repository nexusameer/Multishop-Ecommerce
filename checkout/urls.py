from django.urls import path
from checkout.views import CheckoutView

urlpatterns = [
    path('', CheckoutView.as_view(), name = 'checkout')
]