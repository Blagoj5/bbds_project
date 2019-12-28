from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin/dashboard', views.admindashboard, name='admindashboard'),
    path('activate/<slug:uidb64>/<slug:token>)/', views.activate, name='activate'),
]