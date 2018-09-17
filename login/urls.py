from django.urls import path

from . import views

app_name = "login"

urlpatterns = [
    path('', views.index, name="login"),
    path('register/', views.register, name="register"),
    path('changePassword/', views.changePassword, name="changePassword"),
    path('logout/', views.logout_view, name="logout")
]