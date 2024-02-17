from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from authentication.utils import *
from .forms import *
from .mixins import *


class RegisterUser(UserIsNotAuthenticated, CreateView):
    form_class = RegisterUserForm
    template_name = "authentication/registration/register.html"

    def form_valid(self, form):
        register_user(form)
        return redirect('email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        if email_confirmation(request, uidb64, token):
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'authentication/registration/email_confirmation_sent.html'


class EmailConfirmedView(TemplateView):
    template_name = 'authentication/registration/email_confirmed.html'


class EmailConfirmationFailedView(TemplateView):
    template_name = 'authentication/registration/email_confirmation_failed.html'


def login_user_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                if user_login(request, username, password):
                    return redirect('home')
            return render(request, 'authentication/login.html', {'form': form})
        else:
            form = LoginUserForm()
            return render(request, 'authentication/login.html', {'form': form})
    else:
        return redirect('home')


def logout_user_view(request):
    logout(request)
    return redirect("home")


def user_password_change_email_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password_change(email)
        return redirect('password_change_sent')
    else:
        form = PasswordChangeForm()
        return render(request, 'authentication/password_change/get_email.html', {'form': form})


class PasswordChangeSentView(TemplateView):
    template_name = 'authentication/password_change/password_change_sent.html'


def password_change_view(request, uidb64, token):
    if check_user_email_mixin(uidb64, token):
        if request.POST:
            form = PasswordChangeDoneForm(request.POST)
            if form.is_valid():
                first_password = form.cleaned_data.get('first_password')
                second_password = form.cleaned_data.get('second_password')
                if first_password == second_password:
                    user_password_change(uidb64, first_password)
                    return redirect('login')
            return render(request, 'authentication/password_change/password_change_done.html', {'form': form})
        else:
            form = PasswordChangeDoneForm()
            return render(request, 'authentication/password_change/password_change_done.html', {'form': form})
    else:
        return redirect('home')
