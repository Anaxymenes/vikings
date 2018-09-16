from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('lesson/', views.lesson, name='lesson'),
    path('playerProfile/', views.playerProfile, name="playerProfile"),
]