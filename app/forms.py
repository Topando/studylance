from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .models import *
from django.forms.widgets import HiddenInput


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


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Логин или почта", widget=forms.TextInput(attrs={"class": "form-input"}),
                               label_suffix="")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}),
                               label_suffix="")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', "username", 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
            'email': 'Почта',

        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'age',)


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('subject', 'description', 'price', 'university', 'direction', 'course', "deadline")
        widgets = {'customer_id': HiddenInput(), "deadline": MyDateInput()}


class TaskAnswerForm(forms.ModelForm):
    class Meta:
        model = TaskAnswer
        fields = ('description', 'price')


class PasswordChangeForm(forms.Form):
    email = forms.EmailField(label='Почта', required=True)


class PasswordChangeDoneForm(forms.Form):
    first_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(), validators=[validate_password])
    second_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('subject', 'description', 'price', 'university', 'direction', 'course', "deadline")
        widgets = {"deadline": MyDateInput()}
