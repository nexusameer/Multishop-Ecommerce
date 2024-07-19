from django.urls import path
from products.views import *

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('shop/', ShopView.as_view(), name = 'shop'),
    path('contact/', ContactView.as_view(), name = 'contact'),
]