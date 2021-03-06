from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('lesson/<int:stage_id>/', views.lesson, name='lesson'),
    path('playerProfile/', views.playerProfile, name="playerProfile"),
    path('messages/', views.messages, name="messages"),
    path('message/', views.message, name="message"),
    path('newMessage/', views.newMessage, name="newMessage"),
    path('settings/', views.settings, name="settings"),
    path('reportError/', views.reportError, name="reportError"),
    path('faq/', views.faq, name="faq"),
    path('potion/', views.potion, name="potion"),
    path('changePassword/', views.changePassword, name="changePassword"),
    path('lesson/<int:stage_id>/<int:task_id>/',views.task_data,name="task"),
    path('lesson/<int:stage_id>/excercise',views.exerciseDetails, name="excercise"),
    path('lesson/<int:stage_id>/usePrompt',views.showPrompt, name="usePrompt"),
]