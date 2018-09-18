from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('lesson/<int:stage_id>/', views.lesson, name='lesson'),
    path('playerProfile/', views.playerProfile, name="playerProfile"),
    path('lesson/<int:stage_id>/<int:task_id>/',views.task_data,name="task"),
]