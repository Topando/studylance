from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect

from task_manager.models import Task


def task_create_mixin(request):
    user = User.objects.filter(pk=request.user.id).first()
    if user is not None and user.profile.is_customer:
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
