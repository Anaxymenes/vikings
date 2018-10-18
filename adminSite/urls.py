from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
app_name = 'adminSite'

urlpatterns = [
    path('', views.groups, name='groups'),
    path('responses', views.responses, name='responses'),
    path('responseDetails', views.responseDetails, name='responseDetails'),
    path('excercises', views.excercises, name='excercises'),
    path('excercises/<int:stage_id>/', views.excercisesWithTasks, name='excercisesWithTable'),
    path('excerciseDetails/<int:task_id>/', views.excerciseDetails, name='excerciseDetails'),
    path('newExcercise/<int:stage_id>/', views.newExcercise, name='newExcercise'),
    path('deleteExcercise/<int:stage_id>/<int:task_id>/', views.deleteExcercise, name='deleteExcercise'),
    path('challenges', views.challenges, name='challenges'),
    path('students', views.students, name='students'),
    path('groupDetails/<int:group_id>/', views.groupDetails, name='groupDetails'),
    path('deleteStudent/<int:student_id>/', views.deleteStudent, name='deleteStudent'),
    path('editStudent/<int:student_id>/', views.editStudent, name='editStudent'),
    path('deleteGroup/<int:group_id>/', views.deleteGroup, name='deleteGroup'),
    path('messages', views.messages, name='messages'),
    path('addGroup/',views.addGroup, name='addGroup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)