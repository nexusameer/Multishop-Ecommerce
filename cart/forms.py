from django import forms
from cart.models import *

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ['total_amount']