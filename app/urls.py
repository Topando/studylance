from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('tasks/', AllTasks.as_view(), name='tasks'),
    path('task/<int:task_id>', AllTasks.as_view(), name='task'),
    path("profile/<int:profile_id>/", Profile.as_view(), name="profile"),
    path('profile_update/', views.profile_update, name='profile_update'),
]