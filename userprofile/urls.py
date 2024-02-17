from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("<int:profile_id>/", ProfileView.as_view(), name="profile"),
    #path('profile_update/', views.profile_update, name='profile_update'),
    path("executor-info/", views.executor_info_view, name="executor_info"),
]
