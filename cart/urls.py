from django.urls import path,include
from rest_framework.routers import DefaultRouter
from cart.views import *

# DefaultRouter from Django Rest Framework (DRF) automatically creates the URL configurations for a viewset.
# The CartViewSet is registered with the router. This registration tells DRF to generate the appropriate URL patterns for the viewset methods.
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('cart_view', CartView.as_view(), name='cart_view')
]