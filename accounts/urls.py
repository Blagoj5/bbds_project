from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from .tokens import account_activation_token


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin/dashboard', views.admindashboard, name='admindashboard'),
    path('profile/username/<int:user_id>', views.change_username, name='change_username'), 
    path('profile/password/<int:user_id>', views.change_password, name='change_password'), 
    path('activate/<slug:uidb64>/<slug:token>)/', views.activate, name='activate'),
    path(
    'reset-password/',
        auth_views.PasswordResetView.as_view(
        template_name='accounts/reset_password.html',
        # This is how you do it if you want to have you own custom html email when sending to change pass!!
        # email_template_name=None, 
        # html_email_template_name='accounts/reset_password_email.html',
        success_url=settings.LOGIN_URL,
        token_generator=account_activation_token),
        name='reset_password'
  ),
   path(
        'reset-password-confirmation/<str:uidb64>/<str:token>/',
        auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/reset_password_update.html', 
        token_generator=account_activation_token),
        name='password_reset_confirm'
  ),
]