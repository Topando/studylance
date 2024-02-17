from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import FileResponse
from django.urls import reverse
from django import forms

from studlance import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verify = models.BooleanField(default=False)
    is_executor = models.BooleanField(default=0)
    is_customer = models.BooleanField(default=0)
    photo = models.ImageField(upload_to="profile/", blank=True)
    age = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(default=0)
    rating = models.FloatField(default=5.0)
    count_tasks = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_user_resume(sender, instance, created, **kwargs):
    if created:
        Resume.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_resume(sender, instance, **kwargs):
    instance.resume.save()


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    university = models.ForeignKey('app.University', on_delete=models.CASCADE, null=True, blank=True)
    direction = models.ForeignKey('app.Direction', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey('app.Course', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    contact = models.TextField(null=True, blank=True)


class University(models.Model):
    university = models.CharField(max_length=100)

    def __str__(self):
        return self.university


class Course(models.Model):
    course = models.CharField(max_length=2)

    def __str__(self):
        return self.course


class Direction(models.Model):
    code = models.CharField(max_length=10)
    direction = models.CharField(max_length=100)

    def __str__(self):
        return self.direction


class Task(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_customer', null=True, blank=True)
    executor_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_working = models.BooleanField(default=False)
    subject = models.CharField(max_length=40, verbose_name="Предмет")
    description = models.TextField(verbose_name="Описание")
    university = models.ForeignKey('app.University', verbose_name="ВУЗ", on_delete=models.CASCADE)
    direction = models.ForeignKey('app.Direction', verbose_name="Направление", on_delete=models.CASCADE)
    course = models.ForeignKey('app.Course', verbose_name="Курс", on_delete=models.CASCADE)
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
    description = models.TextField()
    price = models.IntegerField(null=True, blank=True)
