from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
