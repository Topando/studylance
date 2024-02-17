from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('tasks/<int:task_id>/response/', ResponseTask.as_view(), name='task_response'),


]
