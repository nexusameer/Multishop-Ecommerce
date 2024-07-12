from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    

    def get_success_url(self):
        return reverse_lazy('home')
    
class CustomLogoutView(LogoutView):
    
    def get_success_url(self):
        return reverse_lazy('login')

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    