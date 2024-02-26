from django import forms
from django.forms import HiddenInput

from task_manager.models import Task, TaskAnswer


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('subject', 'description', 'price', 'university', 'direction', 'course', "deadline")
        widgets = {"deadline": MyDateInput()}


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('subject', 'description', 'price', 'university', 'direction', 'course', "deadline")
        widgets = {'customer_id': HiddenInput(), "deadline": MyDateInput()}


class TaskAnswerForm(forms.ModelForm):
    class Meta:
        model = TaskAnswer
        fields = ('description', 'price')


