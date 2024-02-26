from django.contrib.auth.models import User
from django.db import models
from django.http import FileResponse
from django.urls import reverse


class Task(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_customer', null=True, blank=True)
    executor_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_working = models.BooleanField(default=False)
    subject = models.CharField(max_length=40, verbose_name="Предмет")
    description = models.TextField(verbose_name="Описание")
    university = models.ForeignKey('University', verbose_name="Университет", on_delete=models.CASCADE)
    direction = models.ForeignKey('Direction', verbose_name="Направление", on_delete=models.CASCADE)
    course = models.ForeignKey('Course', verbose_name="Курс", on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name="Цена", null=True, blank=True)
    deadline = models.DateField(verbose_name="Дедлайн", null=True, blank=True)
    time_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("task", kwargs={"task_id": self.pk})


class ImagesTask(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images_task')
    image = models.FileField(upload_to='tasks/', null=True, blank=True)


class FilesTask(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files_task')
    file = models.FileField(upload_to='tasks/', null=True, blank=True)

    def file_download(self):
        return FileResponse(self.file, as_attachment=True)


class TaskAnswer(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(verbose_name='Отклик')
    price = models.IntegerField(verbose_name='Цена', null=True, blank=True)


class University(models.Model):
    university = models.CharField(verbose_name="Университет", max_length=100)

    def __str__(self):
        return self.university


class Course(models.Model):
    course = models.CharField(verbose_name="Курс", max_length=2)

    def __str__(self):
        return self.course


class Direction(models.Model):
    code = models.CharField(verbose_name="Код", max_length=10)
    direction = models.CharField(verbose_name="Направление", max_length=100)

    def __str__(self):
        return self.direction
