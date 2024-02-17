from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('tasks/', views.all_tasks_view, name='tasks'),
    path('tasks/create/', views.task_create_view, name='task_create'),
    path('tasks/<int:task_id>/', TaskDetail.as_view(), name='task'),
    path('tasks/<int:task_id>/update/', views.task_update_view, name='task_update'),
    path('tasks/<int:task_id>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('delete-img-task/<int:image_id>/', views.delete_img_task_view, name='delete_img_task'),
    path('tasks/response/<int:task_id>/', ResponseTask.as_view(), name='task_response'),
]
