from django.db import models
from django.contrib.auth.models import User
from cart.models import *
from datetime import datetime



class Order(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('delivered', 'Delivered'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('COD', 'COD'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user']),
        ]

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        now = datetime.now()
        user_id = self.user.id if self.user else '0'
        return f'ORDER{now.strftime("%Y%m%d%H%M%S")}{user_id}'

    def __str__(self):
        return f'Order {self.order_number} by {self.name}'
