from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from task_manager.models import Task


def task_create_mixin(user):
    count_tasks = Task.objects.filter(customer_id=user).count()
    if user.is_authenticated and count_tasks < 5:
        return True
    return False


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


def task_update_mixin(user, task_id):
    task = Task.objects.get(pk=task_id)
    if user.is_authenticated and user.pk == task.customer_id.pk:
        return True
    raise PermissionDenied()
