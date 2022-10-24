from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'network_app/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'network_app/login.html'

    def get_success_url(self):
        return reverse_lazy('profile')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')
