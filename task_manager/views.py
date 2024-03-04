from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, CreateView

from task_manager.forms import TaskCreateForm, TaskUpdateForm, TaskAnswerForm
from task_manager.mixins import *
from task_manager.models import TaskAnswer
from task_manager.utils import *


def all_tasks_view(request):
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    per_page = 10
    count_page = per_page * int(page_number)
    next_page = int(page_number) + 1
    tasks = Task.objects.all().order_by('-time_created')[0:count_page]
    if len(Task.objects.all()) > len(tasks):
        is_next_page = True
    else:
        is_next_page = False
    return render(request, "task_manager/all_tasks.html",
                  {"tasks": tasks, "next_page": next_page, "is_next_page": is_next_page})


def task_create_view(request):
    context = {}
    if task_create_mixin(request.user):
        if request.method == "POST":
            form = TaskCreateForm(request.POST)
            images = request.FILES.getlist("images")
            files = request.FILES.getlist("files")
            if form.is_valid():
                if check_files(images) and check_files(files):
                    customer_id = request.user.id
                    customer = User.objects.get(pk=customer_id)
                    form.instance.customer_id = customer
                    task = form.save()
                    images_in_db(images, task)
                    files_in_db(files, task)
                    return redirect('tasks')
                return render(request, "task_manager/task_create.html", context={"form": form})
            return render(request, 'task_manager/task_create.html', {'form': form})
        else:
            form = TaskCreateForm()
            return render(request, 'task_manager/task_create.html', {'form': form})
    else:
        return redirect('home')


class TaskDetail(DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"
    pk_url_kwarg = "task_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = ImagesTask.objects.filter(task_id=self.kwargs["task_id"]).all()
        files = FilesTask.objects.filter(task_id=self.kwargs["task_id"]).all()
        context["images"] = images
        context["files"] = files
        if self.request.user.is_authenticated:
            context['task_answer'] = TaskAnswer.objects.filter(task_id=self.kwargs["task_id"],
                                                               author_id=self.request.user).exists()
        return context


def task_update_view(request, task_id):
    images = ImagesTask.objects.filter(task_id=task_id)
    files = FilesTask.objects.filter(task_id=task_id)
    context = {"images": images, "files": files}
    if task_update_mixin(request.user, task_id):
        if request.method == "POST":
            task = get_task_by_task_id(task_id)
            form = TaskUpdateForm(request.POST, instance=task)
            context["form"] = form
            images = request.FILES.getlist("images")
            files = request.FILES.getlist("files")
            count_images = len(images) + get_count_files_in_task(task_id, ImagesTask)
            count_files = len(files) + get_count_files_in_task(task_id, FilesTask)
            if form.is_valid() and count_images <= 5 and count_files <= 5:
                if check_files(files) and check_files(images):
                    form.save()
                    images_in_db(images, task)
                    files_in_db(files, task)
                    return redirect("task", task_id)
                return render(request, "task_manager/task_update.html", context)
            return render(request, "task_manager/task_update.html", context)
        else:
            task = Task.objects.get(pk=task_id)
            form = TaskUpdateForm(instance=task)
            context['form'] = form
            return render(request, "task_manager/task_update.html", context=context)
    else:
        return redirect("home")


class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    pk_url_kwarg = "task_id"
    template_name = "task_manager/task_delete.html"
    success_url = reverse_lazy("tasks")

    def test_func(self):
        task = get_task_by_task_id(self.kwargs["task_id"])
        customer_id = task.customer_id.id
        executor_id = task.executor_id
        return check_task_delete(self.request.user, customer_id, executor_id)


def delete_img_task_view(request, image_id):
    user_id = get_user_by_image_id(image_id)
    if check_author_task(request.user, user_id):
        image = get_image_by_image_id(image_id)
        task_id = image.task_id.id
        delete_image_by_task(image)
        return redirect("task_update", task_id)
    return redirect('home')


class ResponseTask(ResponseMixin, UserPassesTestMixin, CreateView):
    model = TaskAnswer
    form_class = TaskAnswerForm
    template_name = "task_manager/response_task.html"
    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.author_id = self.request.user
        task = Task.objects.filter(id=self.kwargs["task_id"]).first()
        form.instance.task_id = task
        form.save()
        return redirect("task", self.kwargs["task_id"])


@login_required
def all_responses_task_view(request, task_id):
    user_id = Task.objects.get(pk=task_id).customer_id.pk
    if check_author_task(request.user, user_id):
        context = {}
        context['responses'] = TaskAnswer.objects.filter(task_id=task_id)
        return render(request, 'task_manager/all_responses_task.html', context)
    else:
        raise PermissionDenied()


@login_required
def all_tasks_user_view(request):
    context = {}
    user_id = request.user.id
    tasks = Task.objects.filter(customer_id=user_id)
    context['tasks'] = tasks
    return render(request, 'task_manager/all_tasks_user.html', context=context)


@login_required
def all_responses_user_view(request):
    context = {}
    user_id = request.user.id
    responses = TaskAnswer.objects.filter(author_id=user_id)
    context['responses'] = responses
    return render(request, 'task_manager/all_responses_user.html', context=context)


def update_response(request, response_id):
    context = {}
    response = TaskAnswer.objects.get(pk=response_id)
    if request.user.pk == response.author_id.pk:
        if request.method == 'POST':
            form = TaskAnswerForm(request.POST, instance=response)
            if form.is_valid():
                form.save()
                return redirect('task_my_responses')
            else:
                context['form'] = form
                return render(request, 'task_manager/update_response.html', context=context)
        else:
            context['form'] = TaskAnswerForm(instance=response)
            return render(request, 'task_manager/update_response.html', context=context)
    else:
        raise PermissionDenied()


def delete_response(request, response_id):
    response = TaskAnswer.objects.get(pk=response_id)
    if request.user.pk == response.author_id.pk:
        if request.method == 'POST':
            response.delete()
            return redirect('task_my_responses')
        else:
            return render(request, 'task_manager/response_delete.html')
    else:
        raise PermissionDenied()


def set_response_task(request, response_id):
    response = TaskAnswer.objects.get(pk=response_id)
    task = response.task_id
    if request.user.pk == task.customer_id.pk and task.executor_id is None:
        task.executor_id = response.author_id
        task.save()
        return redirect('task', task.pk)
    else:
        raise PermissionDenied()