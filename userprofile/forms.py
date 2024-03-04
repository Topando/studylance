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


class UpdateProfileForm(forms.Form):
    age = forms.IntegerField(label="Возвраст", min_value=16, max_value=100)

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)


class UpdateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('description', 'university', 'direction', 'course', 'contact')
        labels = {
            'university': 'Университет',
            'direction': 'Направление',
            "course": 'Курс',
        }


class UpdateProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)

    def __init__(self, *args, **kwargs):
        super(UpdateProfilePhotoForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'profile_photo'})
        self.fields['photo'].label = ""
