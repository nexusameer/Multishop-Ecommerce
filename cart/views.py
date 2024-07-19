from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from cart.models import *
from cart.serializers import *
from rest_framework. response import Response
from rest_framework.decorators import action
from rest_framework import serializers, viewsets


# Create your views here.
class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cart_items = CartItem.objects.all()
        context['cart_items'] = cart_items
        return context

class CartViewSet(viewsets.ViewSet):
    def retrieve_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        cart_item.save()
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_cart_item(self, request):
        cart = Cart.objects.get(user=request.user)
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity = int(quantity)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def _remove_cart_item(self, cart_item):
        cart_item.delete()
        cart = cart_item.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods = ['post'])
    def remove_cart_item(self, request):
        cart_item_id = request.data.get('cart_item_id')
        cart_item = CartItem.objects.get(id=cart_item_id)
        return self._remove_cart_item(cart_item)
    
    @action(detail=False, methods = ['post'])
    def increment_quantity(self, request):
        cart_item_id = request.data.get('cart_item_id')
        cart_item = CartItem.objects.get(id = cart_item_id)
        cart_item.quantity +=1
        cart_item.save()

        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data)

    @action(detail=False, methods = ['post'])
    def decrement_quantity(self, request):
        cart_item_id = request.data.get('cart_item_id')
        cart_item = CartItem.objects.get(id= cart_item_id)
        cart_item.quantity -=1
        cart_item.save()

        if cart_item.quantity == 0:
            self._remove_cart_item(cart_item)
        

        serializer = CartSerializer(cart_item.cart)
        return Response(serializer.data)
    