from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.programsView, name='programs'),
    path('<slug:slug_field>', views.programView, name='program')
]