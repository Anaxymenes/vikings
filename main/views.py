from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from models.models import *
import logging
from datetime import datetime, timedelta
from .msgUtil import *

import random
logger = logging.getLogger(__name__)

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser :
            return HttpResponseRedirect(reverse('adminSite:groups'))
        return render(request, 'main/index.html', {})
    return HttpResponseRedirect(reverse('login:login'))

def lesson(request,stage_id):
    if request.user.is_authenticated:
        user = User.objects.filter(id=request.user.id).first()
        stage = Stage.objects.filter(id=stage_id).first()
        stageStudent = StageStudent.objects.filter(student=user).filter(stage=stage).first()
        currentTasks = Answer.objects.filter(stageStudent=stageStudent)
        if currentTasks.count()==0 :
            createTaskForStudent(user,stage)
            currentTasks = Answer.objects.filter(stageStudent=stageStudent)
        return render(request, 'main/lesson.html', {
            "stage":stage,
            "tasks":currentTasks,
        })
    return HttpResponseRedirect(reverse('login:login'))

def exerciseDetails(request, stage_id):
    if request.method == "POST":
        action = request.POST.get('action')
        if action == "save" or action == "close":
            answer_id = request.POST.get('taskId')
            usedPrompt = request.POST.get('usedPrompt')
            answerSql = request.POST.get('answerSql')
            student = User.objects.filter(id=request.user.id).first()
            stage = Stage.objects.filter(id=stage_id).first()
            stageStudent = StageStudent.objects.filter(student=student).filter(stage=stage).first()
            answer = Answer.objects.filter(id=answer_id).filter(stageStudent=stageStudent).first()
            answer.answerSql = answerSql
            answer.usedPrompt = usedPrompt
            if action == "close":
                answer.completed = 1
                answer.completed_at = datetime.now()
            answer.save()
        task = StageTasks.objects.filter(id=request.POST.get('taskId')).first()
        stage = Stage.objects.filter(id=stage_id).first()
        answer = Answer.objects.filter(task=task).filter(stageStudent=getStageStudentByStageId(request.user,stage_id)).first()
        difficultyLevel = DifficultyLevel.objects.filter(id = task.difficulty_level.id).first()
        story = StoryLevel.objects.filter(stage = stage).filter(difficulty_level = difficultyLevel).first()
        return render(request, 'main/excercise.html', {"answer" : answer, "task":task,'story':story})
    else :
        return render(request, 'main/index.html', {})

def showPrompt(request, stage_id):
    if request.method == "POST":
        print(request.POST)
        answer = Answer.objects.filter(id=request.POST.get('answerId')).filter(stageStudent=getStageStudentByStageId(request.user,stage_id)).first()
        setattr(answer,'usedPrompt',1)
        answer.save()
    return exerciseDetails(request,stage_id)

def playerProfile(request):
    if request.user.is_authenticated:
        achievements_id_list = AchievementTask.objects.filter(student=request.user).values_list('achievement')
        achivements = Achievement.objects.filter(id__in = achievements_id_list)
        answers = []
        stagesStudent = StageStudent.objects.filter(student = request.user)
        for stageStudent in stagesStudent:
            for answer in Answer.objects.filter(stageStudent=stageStudent):
                answers.append(answer)
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
    user = User.objects.filter(id=request.user.id).first()
    errors = None
    if request.method == 'POST':
        content = request.POST.get('messageContent')
        title = request.POST.get('messageTopic')
        studentGroup = StudentGroup.objects.filter(student=user).first()
        group = Group.objects.filter(id = studentGroup.group.id).first()
        lecturer = User.objects.filter(id=group.lecturer.id).first()
        
        if request.POST.get('answer_to_message').exists():
            answer_to_message = request.POST.get('answer_to_message')
            msg = Messages.objects.filter(id=answer_to_message)
            error = createMessageAnswer(msg,user,lecturer,content,title)
        else :
            error = createMessage(user,lecturer,content,title)
    msgs = getAllMessagesByUser(user)
    print(errors)
    return render(request, 'main/messages.html',{'messages':msgs, 'error': errors})

def message(request):
    msg = None
    if request.method == 'POST':
        message_id = request.POST.get('message')
        user = User.objects.filter(id = request.user.id).first()
        msg = getMessageDetails(message_id,user)
        return render(request, 'main/message.html',{'message':msg})
    return render(request, 'main/message.html',{'message':msg})

def newMessage(request):
    msg = None
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        if message_id != None:
            msg = Messages.objects.filter(id=message_id).first()
    return render(request, 'main/newMessage.html',{'message':msg})

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

def getStageStudentByStageId(user, stage_id):
    stage = Stage.objects.filter(id=stage_id).first()
    stageStudent = StageStudent.objects.filter(student=user).filter(stage=stage).first()
    return stageStudent

def createStageStudent(stage, user):
    stageStudent = StageStudent.objects.create(
        stage = stage,
        student = user,
        databaseSql = "",
        complete = 0,
        start_at = datetime.now(),
        end_at = datetime.now()+timedelta(days=7)
    )
    return stageStudent

def createTaskForStudent(user, stage):
    stageStudent = StageStudent.objects.filter(student=user).filter(stage=stage).first()
    if stageStudent == None:
        createStageStudent(stage,user)
        stageStudent = StageStudent.objects.filter(student=user).filter(stage=stage).first()
    levels = DifficultyLevel.objects.all()[:6]
    for x in levels:
        stageTasks = StageTasks.objects.filter(stage=stage).filter(difficulty_level=x).order_by("?")[:1]
        for task in stageTasks:
            Answer.objects.create(
                answerSql = "",
                stageStudent = stageStudent,
                task = task,
                usedPrompt = 0,
                note = 0,
                completed = 0,
                rated = 0
                )
    return True

def getAnswer(task,user,stage_id):
    answer = Answer.objects.filter(task=task).filter(stageStudent=getStageStudentByStageId(user,stage_id)).first()
    return answer

