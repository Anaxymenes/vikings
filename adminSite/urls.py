from django.urls import path

from . import views

app_name = 'adminSite'

urlpatterns = [
    path('', views.adminSite, name='adminSite')
]