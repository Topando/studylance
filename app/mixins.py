from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import Task


class ResponseMixin(UserPassesTestMixin):
    def test_func(self):
        user_id = self.request.user.pk
        task_id = self.kwargs["task_id"]
        if user_id == Task.objects.get(pk=task_id).customer_id.id:
            return False
        if not self.request.user.profile.is_executor:
            return False
        return True

    def handle_no_permission(self):
        return redirect('home')


class UserIsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect('home')
