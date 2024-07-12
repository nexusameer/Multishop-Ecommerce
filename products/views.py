from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import *
from typing import Any
from django.db.models import Q
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(*args,**kwargs)
        # products = Product.objects.all()
        # context['products'] = products
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['products'] = Product.objects.filter(
                Q(name__icontains=search_input) |
                Q(org_price__icontains=search_input) |
                Q(category__name__icontains=search_input)
                )
        else:
            context['products'] = Product.objects.all()

        return context