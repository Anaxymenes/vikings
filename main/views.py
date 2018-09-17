from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from models.models import AccountDetails, Stage, StageTasks

import random

def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html', {})
    return HttpResponseRedirect(reverse('login:login'))

def lesson(request,stage_id):
    if request.user.is_authenticated:
        task_id = None
        task = None
        if request.method == 'GET':
            task_id = request.GET.get('task_id')
            print(task_id)
        stage = Stage.objects.filter(id=stage_id).first()
        stageTasks = StageTasks.objects.filter(stageId=stage).order_by("?")[:5]
        return render(request, 'main/lesson.html', {
            "stage":stage,
            "tasks":stageTasks,
            "current_task": task,
        })
    return HttpResponseRedirect(reverse('login:login'))

def playerProfile(request):
    if request.user.is_authenticated:
        return render(request, 'main/playerProfile.html', {})
    return HttpResponseRedirect(reverse('login:login'))

