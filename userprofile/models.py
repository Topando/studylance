from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_executor = models.BooleanField(default=0)
    photo = models.ImageField(upload_to="profile/", blank=True)
    age = models.IntegerField(verbose_name="Возвраст", blank=True, null=True, validators=[MinValueValidator(0),
                                                                                          MaxValueValidator(100)])
    balance = models.IntegerField(verbose_name="Баланс", default=0)
    rating = models.FloatField(verbose_name="Рейтинг", default=5.0)
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
    rating = models.IntegerField(verbose_name="Оценка")


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    university = models.ForeignKey('task_manager.University', on_delete=models.CASCADE, null=True, blank=True)
    direction = models.ForeignKey('task_manager.Direction', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey('task_manager.Course', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(verbose_name="Описание профиля", null=True, blank=True)
    contact = models.TextField(verbose_name="Контакты", null=True, blank=True)
