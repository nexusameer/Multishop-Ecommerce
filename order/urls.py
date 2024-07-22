from django.urls import path
from order.views import *
urlpatterns =[
    path('', OrderView.as_view(), name = 'order')
]