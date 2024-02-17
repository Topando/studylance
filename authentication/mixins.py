from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode


class UserIsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect('home')


def check_user_email_mixin(uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        return True
    return False
