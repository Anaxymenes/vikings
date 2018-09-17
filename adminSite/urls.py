from django.urls import path

from . import views

app_name = 'adminSite'

urlpatterns = [
    path('', views.groups, name='groups'),
    path('responses', views.responses, name='responses'),
    path('excercises', views.excercises, name='excercises'),
]