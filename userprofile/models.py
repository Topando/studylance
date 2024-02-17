from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_author')
    comment = models.TextField()


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    university = models.ForeignKey('task_manager.University', on_delete=models.CASCADE, null=True, blank=True)
    direction = models.ForeignKey('task_manager.Direction', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey('task_manager.Course', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    contact = models.TextField(null=True, blank=True)
