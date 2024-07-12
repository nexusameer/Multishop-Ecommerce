from django.urls import path
from products.views import *

urlpatterns = [
    path('', HomeView.as_view(), name = 'home')
]