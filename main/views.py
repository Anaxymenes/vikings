from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from models.models import AccountDetails, Stage, StageTasks, AchievementTask, Achievement, Answer, UserAbsence
import logging

import random
logger = logging.getLogger(__name__)

def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html', {})
    return HttpResponseRedirect(reverse('login:login'))

def lesson(request,stage_id):
    if request.user.is_authenticated:
        stage = Stage.objects.filter(id=stage_id).first()
        currentTasks = Answer.objects.filter(stage=stage).filter(student=request.user)
        if currentTasks.count()==0 :
            for x in range(1,6):
                stageTasks = StageTasks.objects.filter(stage=stage).filter(difficulty_level=x).order_by("?")[:1]
                for task in stageTasks:
                    Answer.objects.create(
                        answerSql = "",
                        stage = stage,
                        student = request.user,
                        task = task,
                        usedPrompt = 0,
                        note = 0,
                        completed = 0
                    )
            currentTasks = Answer.objects.filter(stage=stage).filter(student=request.user).order_by('task.difficult_level')
        return render(request, 'main/lesson.html', {
            "stage":stage,
            "tasks":currentTasks,
        })
    return HttpResponseRedirect(reverse('login:login'))

def exerciseDetails(request, stage_id):
    if request.method == "POST":
        task = StageTasks.objects.filter(id=request.POST.get('taskId')).first()
        answer = Answer.objects.filter(task=task).filter(student=request.user).first()
        return render(request, 'main/excercise.html', {"answer" : answer, "task":task})
    else :
        return render(request, 'main/index.html', {})

def showPrompt(request, stage_id):
    if request.method == "POST":
        answer = Answer.objects.filter(id=request.POST.get('answerId')).filter(student=request.user).first()
        setattr(answer,'usedPrompt',1)
        answer.save()
    return exerciseDetails(request,stage_id)

def playerProfile(request):
    if request.user.is_authenticated:
        achievements_id_list = AchievementTask.objects.filter(student=request.user).values_list('achievement')
        achivements = Achievement.objects.filter(id__in = achievements_id_list)
        answers = Answer.objects.filter(student=request.user).filter(completed=1)
        absences = UserAbsence.objects.filter(student=request.user).order_by('date')
        max_points = 0
        actual_points = 0
        result_points = 0
        for answer in answers:
            task = getattr(answer,"task")
            max_points += getattr(task,"points")
            actual_points += getattr(task,"points") * (getattr(answer,"note") / 100)
        if max_points != 0 :
            result_points = actual_points * 100 / max_points
        return render(request, 'main/playerProfile.html', {
            "achievements" : achivements,
            "answers":answers,
            "results_points": result_points,
            "absences":absences,
        })
    return HttpResponseRedirect(reverse('login:login'))

def messages(request):
    return render(request, 'main/messages.html')

def message(request):
    return render(request, 'main/message.html')

def settings(request):
    return render(request, 'main/settings.html')

def excercise(request):
    prompt = False
    return render(request, 'main/excercise.html', {"prompt": prompt })

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