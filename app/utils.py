from itertools import count

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import User, Task, ImagesTask, FilesTask


def check_author_task(user, pk):
    if user.pk == pk:
        return True
    return False


def check_is_executor(executor_id):
    if executor_id is None:
        return True
    return False


def check_task_delete(user, pk, executor_id):
    if check_author_task(user, pk) and check_is_executor(executor_id):
        return True
    return False


def check_create_task(user, Task):
    count_tasks = Task.objects.filter(customer_id=user.id).count()
    if count_tasks > 10:
        return False
    if not user.profile.is_customer:
        return False
    return True


class GetUser:
    def get_user_pk(self, pk):
        return User.objects.filter(id=pk).first()

    def get_user_email(self, email):
        return User.objects.filter(email=email).first()


def password_change(email):
    user = User.objects.filter(email=email).first()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_url = reverse_lazy('password_change_check', kwargs={'uidb64': uid, 'token': token})
    current_site = Site.objects.get_current().domain
    subject = 'Изменение пароля'
    message = f'Чтобы изменить пароль перейдите по ссылке: http://{current_site}{activation_url}'
    send_message(email, subject, message)


def send_message(email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )


def user_password_change(uidb64, password):
    uid = urlsafe_base64_decode(uidb64).decode('utf-8')
    user = User.objects.get(pk=uid)
    password = make_password(password)
    user.password = password
    user.save()


def user_login(request, username, password):
    user = User.objects.filter(email=username).first()
    if user is None:
        user = User.objects.filter(username=username).first()
    print(password)
    if user is not None and check_password(password, user.password):
        login(request, user)
        print("Пользователь авторизован")
        return True
    return False


def register_user(form):
    user = form.save(commit=False)
    user.is_active = False
    user.save()

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
    current_site = Site.objects.get_current().domain
    subject = 'Подтвердите свой электронный адрес'
    message = f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}'
    email = user.email
    send_message(email, subject, message)


def task_create(task_info, images, files):
    task = Task.objects.create(customer_id=task_info['user'], title=task_info['title'],
                               description=task_info['description'], price=task_info['price'],
                               university=task_info['university'], direction=task_info['direction'],
                               course=task_info['course'])
    images_in_db(images, task)
    files_in_db(files, task)


def images_in_db(images, task):
    for image in images:
        ImagesTask.objects.create(task_id=task, image=image)


def files_in_db(files, task):
    for file in files:
        FilesTask.objects.create(task_id=task, file=file)


def get_user_by_image_id(image_id):
    user_id = ImagesTask.objects.filter(pk=image_id).first().task_id.customer_id.id
    return user_id


def get_image_by_image_id(image_id):
    return ImagesTask.objects.filter(pk=image_id).first()


def delete_image(image):
    try:
        image.delete()
    except Exception:
        print("Ошибка удаления фотографии")


def get_task_by_task_id(task_id):
    return Task.objects.get(pk=task_id)


def get_form_task_info(form):
    task_info = {}
    task_info['title'] = form.cleaned_data.get("title")
    task_info['description'] = form.cleaned_data.get("description")
    task_info['price'] = form.cleaned_data.get("price")
    task_info['university'] = form.cleaned_data.get("university")
    task_info['direction'] = form.cleaned_data.get("direction")
    task_info['course'] = form.cleaned_data.get("course")
    return task_info


def update_task(task_id, task_info):
    task = Task.objects.get(pk=task_id)
    task.title = task_info.get('title')
    task.description = task_info.get('description')
    task.price = task_info.get('price')
    task.university = task_info.get('university')
    task.direction = task_info.get('direction')
    task.course = task_info.get('course')
    task.save()


def get_count_files_in_task(task_id, obj):
    return obj.objects.filter(task_id=task_id).count()