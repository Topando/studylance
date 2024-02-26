from django import forms
from django.contrib.auth.models import User

from userprofile.models import Profile, Resume


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', "username", 'email')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин',
            'email': 'Почта', }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('age', )


class UpdateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('description', 'university', 'direction', 'course', 'contact')
        labels = {
            'university': 'Университет',
            'direction': 'Направление',
            "course": 'Курс',
        }