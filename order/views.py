from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse, render
from django.db.models import Sum
from cart.models import Checkout
from .models import Order

class OrderView(TemplateView):
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['pending_checkouts'] = Checkout.objects.filter(user=user, status='pending')
        return context

    def post(self, request, *args, **kwargs):

        user = request.user
        checkout_ids = request.POST.getlist('checkout_ids')
        checkouts = Checkout.objects.filter(id__in=checkout_ids, user=user, status='pending')

        if not checkouts.exists():
            # Handle the case where there are no pending checkouts for the user
            return render(request, 'error.html')

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        total_amount = checkouts.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Create an Order object
        order = Order.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            zip_code=zip_code,
            status='draft',  # Set initial status to 'draft'
            payment_method=request.POST.get('payment_method'),
            total_amount=total_amount
        )

        # Link the checkouts to the order
        order.checkouts.set(checkouts)
        order.save()

        for i in checkouts:
            checkouts.update(status='ordered')

        return redirect(reverse('home'))
