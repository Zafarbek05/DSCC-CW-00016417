from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('register/', views.register, name='register'),
]