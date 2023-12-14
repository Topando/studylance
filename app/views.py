from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from app.forms import *

from app.db_handler.db_update import database_filling
from app.utils import *


def index(request):
    return render(request, 'app/index.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "app/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "app/login.html"

    def get_success_url(self):
        return reverse_lazy("home")


def logout_user(request):
    logout(request)
    return redirect("home")


class Profile(DetailView):
    model = User
    template_name = "app/profile.html"
    pk_url_kwarg = "profile_id"


def profile_update(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, "app/profile_update.html", {
            'user_form': user_form,
            'profile_form': profile_form
        })


class AllTasks(ListView):
    model = Task
    template_name = "app/all_tasks.html"
    context_object_name = "tasks"


class TaskDetail(DetailView):
    model = Task
    template_name = "app/task_detail.html"
    pk_url_kwarg = "task_id"


class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    pk_url_kwarg = "task_id"
    template_name = "app/task_update.html"
    form_class = TaskUpdateForm

    def form_valid(self, form):
        form.save()
        return redirect("task", self.kwargs["task_id"])

    def test_func(self):
        customer_id = Task.objects.get(pk=self.kwargs["task_id"]).customer_id.id
        return check_author_task(self.request.user, customer_id)


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    pk_url_kwarg = "task_id"
    template_name = "app/task_delete.html"
    success_url = reverse_lazy("tasks")

    def test_func(self):
        task = Task.objects.get(pk=self.kwargs["task_id"])
        customer_id = task.customer_id.id
        executor_id = task.executor_id
        return check_task_delete(self.request.user, customer_id, executor_id)


class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "app/task_update.html"

    def form_valid(self, form):
        form.instance.customer_id = self.request.user
        form.save()
        return redirect("tasks")

    def test_func(self):
        return True
