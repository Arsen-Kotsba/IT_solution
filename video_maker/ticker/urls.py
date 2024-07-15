from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Маршрут для формы
    path('create_video/', views.create_video, name='create_video'),  # Маршрут для создания видео
]