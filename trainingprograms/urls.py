from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.programsView, name='programs'),
    path('<slug:program_name>', views.programView, name='program')
]