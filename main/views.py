from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from models.models import AccountDetails, Stage, StageTasks, AchievementTask, Achievement

import random

def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html', {})
    return HttpResponseRedirect(reverse('login:login'))

def lesson(request,stage_id):
    if request.user.is_authenticated:
        
        stage = Stage.objects.filter(id=stage_id).first()
        stageTasks = StageTasks.objects.filter(stage=stage).order_by("?")[:5]
        
        return render(request, 'main/lesson.html', {
            "stage":stage,
            "tasks":stageTasks,
        })
    return HttpResponseRedirect(reverse('login:login'))

def playerProfile(request):
    if request.user.is_authenticated:
        achievements_id_list = AchievementTask.objects.filter(student=request.user).values_list('achievement')
        print(achievements_id_list)
        achivements = Achievement.objects.filter(id__in = achievements_id_list)
        print(achivements)
        return render(request, 'main/playerProfile.html', {
            "achievements" : achivements

        })
    return HttpResponseRedirect(reverse('login:login'))

def task_data(request, stage_id, task_id):
    current_task = StageTasks.objects.filter(id=task_id).first()    
    data = {
        "title" : current_task.title,
        "description" : current_task.description,
        "points" : current_task.points,
        "exp_points" : current_task.exp_points,
        "current_task" : current_task,
    }
    return HttpResponse(data)