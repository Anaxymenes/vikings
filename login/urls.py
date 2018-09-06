from django.urls import path

from . import views

app_name='login'
urlpatterns= [
<<<<<<< HEAD
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
=======
    path('', views.index, name="user_login"),
    path('register/',views.register, name='register'),
>>>>>>> 32c13168b4c1411ffbbea49a39c3ec3432969980
    path('changePassword/', views.changePassword, name='changePassword'),
]