from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("<int:profile_id>/", views.profile_view, name="profile"),
    path('profile_update/', views.update_profile_view, name='profile_update'),
    path("executor-info/", views.executor_info_view, name="executor_info"),
]
