from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def user_login(request, username, password):
    user = User.objects.filter(email=username).first()
    if user is None:
        user = User.objects.filter(username=username).first()
    if user is not None and check_password(password, user.password):
        login(request, user)
        print("Пользователь авторизован")
        return True
    return False


def register_user(form):
    user = form.save(commit=False)
    print(form.instance.email)
    user.is_active = False
    user.save()

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
    current_site = Site.objects.get_current().domain
    subject = 'Подтвердите свой электронный адрес'
    message = f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}'
    email = user.email
    send_message(email, subject, message)


def send_message(email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


User = get_user_model()


def email_confirmation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return True
    else:
        return False


def password_change(email):
    user = User.objects.filter(email=email).first()
    try:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_url = reverse_lazy('password_change_check', kwargs={'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current().domain
        subject = 'Изменение пароля'
        message = f'Чтобы изменить пароль перейдите по ссылке: http://{current_site}{activation_url}'
        send_message(email, subject, message)
    except Exception as e:
        return redirect("home")


def user_password_change(uidb64, password):
    uid = urlsafe_base64_decode(uidb64).decode('utf-8')
    user = User.objects.get(pk=uid)
    password = make_password(password)
    user.password = password
    user.save()
