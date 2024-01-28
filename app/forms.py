from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.forms.widgets import HiddenInput
from django.core.exceptions import ValidationError


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", 'username', "email", "password1", "password2")


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', "username", 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'age',)


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'price', 'university', 'direction', 'course')
        widgets = {'customer_id': HiddenInput()}


class TaskAnswerForm(forms.ModelForm):
    class Meta:
        model = TaskAnswer
        fields = ('description', 'price')


class PasswordChangeForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)


class PasswordChangeDoneForm(forms.Form):
    first_password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), validators=[validate_password])
    second_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'price', 'university', 'direction', 'course')


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


def val(value):
    print(value)


class FileFieldForm(forms.Form):
    file_field = MultipleFileField(label="Фото", validators=[val])
    file_field.widget.attrs.update({'accept': 'image/png, image/jpeg, image/jpg'})
