from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView
from app.forms import *
from app.mixins import *
from app.utils import *

User = get_user_model()


def user_password_change_email_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password_change(email)
        return redirect('password_change_sent')
    else:
        form = PasswordChangeForm()
        return render(request, 'app/password_change/get_email.html', {'form': form})


class PasswordChangeSentView(TemplateView):
    template_name = 'app/password_change/password_change_sent.html'


def password_change_view(request, uidb64, token):
    if check_user_email_mixin(uidb64, token):
        if request.POST:

            form = PasswordChangeDoneForm(request.POST)
            if form.is_valid():
                first_password = form.cleaned_data.get('first_password')
                second_password = form.cleaned_data.get('second_password')
                if first_password == second_password:
                    print(first_password)
                    user_password_change(uidb64, first_password)
                    return redirect('login')
            return render(request, 'app/password_change/password_change_done.html', {'form': form})
        else:
            form = PasswordChangeDoneForm()
            return render(request, 'app/password_change/password_change_done.html', {'form': form})
    else:
        return redirect('home')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'app/registration/email_confirmation_sent.html'


class EmailConfirmedView(TemplateView):
    template_name = 'app/registration/email_confirmed.html'


class EmailConfirmationFailedView(TemplateView):
    template_name = 'app/registration/email_confirmation_failed.html'


def index(request):
    return render(request, 'app/index.html')


class RegisterUser(UserIsNotAuthenticated, CreateView):
    form_class = RegisterUserForm
    template_name = "app/registration/register.html"

    def form_valid(self, form):
        register_user(form)
        return redirect('email_confirmation_sent')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                if user_login(request, username, password):
                    return redirect('home')
            return render(request, 'app/login.html', {'form': form})
        else:
            form = LoginUserForm()
            return render(request, 'app/login.html', {'form': form})
    else:
        return redirect('home')


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = ImagesTask.objects.filter(task_id=self.kwargs["task_id"]).all()
        files = FilesTask.objects.filter(task_id=self.kwargs["task_id"]).all()
        context["images"] = images
        context["files"] = files
        return context


class TaskUpdate(TaskUpdateMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    pk_url_kwarg = "task_id"
    template_name = "app/task_update.html"
    form_class = TaskUpdateForm

    def form_valid(self, form):
        form.save()
        return redirect("task", self.kwargs["task_id"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = ImagesTask.objects.filter(task_id=self.kwargs["task_id"])
        return context


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    pk_url_kwarg = "task_id"
    template_name = "app/task_delete.html"
    success_url = reverse_lazy("tasks")

    def test_func(self):
        task = get_task_by_task_id(self.kwargs["task_id"])
        customer_id = task.customer_id.id
        executor_id = task.executor_id
        return check_task_delete(self.request.user, customer_id, executor_id)


# class TaskCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Task
#     form_class = TaskUpdateForm
#     template_name = "app/task_update.html"
#
#     def form_valid(self, form):
#         form.instance.customer_id = self.request.user
#         form.save()
#         return redirect("tasks")
#
#     def test_func(self):
#         return check_create_task(self.request.user, Task)


def task_create_view(request):
    if task_create_mixin(request):
        if request.method == "POST":
            form = TaskCreateForm(request.POST)
            images = request.FILES.getlist("images")
            files = request.FILES.getlist("files")
            if form.is_valid() and len(images) <= 5 and len(files) <= 5:
                task_info = {}
                task_info['title'] = form.cleaned_data.get("title")
                task_info['description'] = form.cleaned_data.get("description")
                task_info['price'] = form.cleaned_data.get("price")
                task_info['university'] = form.cleaned_data.get("university")
                task_info['direction'] = form.cleaned_data.get("direction")
                task_info['course'] = form.cleaned_data.get("course")
                customer_id = request.user.id
                task_info['user'] = User.objects.get(pk=customer_id)
                task_create(task_info, images, files)
                return redirect('tasks')
            return render(request, 'app/task_create.html', {'form': form})
        else:
            form = TaskCreateForm()
            return render(request, 'app/task_create.html', {'form': form})
    else:
        return redirect('home')


class ResponseTask(ResponseMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TaskAnswer
    form_class = TaskAnswerForm
    template_name = "app/response_task.html"
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.author_id = self.request.user
        task = Task.objects.filter(id=self.kwargs["task_id"]).first()
        form.instance.task_id = task
        form.save()
        return redirect("task", self.kwargs["task_id"])


def delete_img_task_view(request, image_id):
    user_id = get_user_by_image_id(image_id)
    if check_author_task(request.user, user_id):
        image = get_image_by_image_id(image_id)
        task_id = image.task_id.id
        delete_image(image)
        return redirect("task_update", task_id)
    return redirect('home')
