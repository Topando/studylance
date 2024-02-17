from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user_view, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('password-change/', views.user_password_change_email_view, name='password_change'),
    path('password-change/<str:uidb64>/<str:token>/', views.password_change_view, name='password_change_check'),
    path('password-change-sent/', PasswordChangeSentView.as_view(), name='password_change_sent'),
]
