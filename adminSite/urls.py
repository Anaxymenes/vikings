from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
app_name = 'adminSite'

urlpatterns = [
    path('', views.groups, name='groups'),
    path('responses', views.responses, name='responses'),
    path('excercises', views.excercises, name='excercises'),
    path('groupDetails', views.groupDetails, name='groupDetails'),
    path('addGroup/',views.addGroup, name='addGroup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)