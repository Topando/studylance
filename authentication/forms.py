from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Логин или почта", widget=forms.TextInput(attrs={"class": "form-input"}),
                               label_suffix="")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}),
                               label_suffix="")


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", 'username', "email", "password1", "password2")


class PasswordChangeForm(forms.Form):
    email = forms.EmailField(label='Почта', required=True)


class PasswordChangeDoneForm(forms.Form):
    first_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(), validators=[validate_password])
    second_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())
