from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode

from .db_handler.db_update import database_filling
from .models import Task
from .utils import check_task_delete
from .views import User


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


def check_user_email_mixin(uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        return True
    return False


def task_create_mixin(request):
    user = User.objects.filter(pk=request.user.id).first()
    if user is not None and user.profile.is_executor:
        return True
    return False


class TaskUpdateMixin(UserPassesTestMixin):
    def test_func(self):
        task = Task.objects.get(pk=self.kwargs["task_id"])
        customer_id = task.customer_id.id
        executor_id = task.executor_id
        return check_task_delete(self.request.user, customer_id, executor_id)