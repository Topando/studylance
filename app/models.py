from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
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
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True, blank=True)
    direction = models.ForeignKey('Direction', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
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


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_author')
    comment = models.TextField()




class Task(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_customer', null=True, blank=True)
    executor_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    is_working = models.BooleanField(default=False)
    title = models.TextField()
    description = models.TextField()
    university = models.ForeignKey('University', on_delete=models.CASCADE)
    direction = models.ForeignKey('Direction', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    time_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("task", kwargs={"task_id": self.pk})


class ImagesTask(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images_task')
    image = models.FileField(upload_to='tasks/', null=True, blank=True)

    def deleter(self):
        print(123)
        return "123"

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


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadFileForm(forms.Form):
    files = MultipleFileField()
