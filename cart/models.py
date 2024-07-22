from django.db import models
from django.contrib.auth.models import User
from products.models import *
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Cart of {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'
    

class Checkout(models.Model):
    STATUS_CHOICES ={
        'pending' : 'pending',
        'ordered' : 'ordered'
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.total_amount}'

class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='checkout_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.checkout.user.username} have {self.quantity} quantity of {self.product.name} in checkout {self.checkout.id}'
    