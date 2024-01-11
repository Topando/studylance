from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('login/', LoginUser.as_view(), name='login'),
    path('tasks/', AllTasks.as_view(), name='tasks'),
    path('tasks/<int:task_id>/', TaskDetail.as_view(), name='task'),
    path('tasks/create/', TaskCreate.as_view(), name='task_create'),
    path('tasks/<int:task_id>/update/', TaskUpdate.as_view(), name='task_update'),
    path('tasks/<int:task_id>/delete/', TaskDelete.as_view(), name='task_delete'),
    path('tasks/<int:task_id>/response/', ResponseTask.as_view(), name='task_response'),
    path("profile/<int:profile_id>/", Profile.as_view(), name="profile"),
    path('profile_update/', views.profile_update, name='profile_update'),
]
