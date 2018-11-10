from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.hashers import make_password, check_password
from models.models import *
from io import BytesIO
from openpyxl import load_workbook, workbook, cell
from .forms import CreateGroup
from django.contrib.auth.models import User
from django.db import transaction
import operator
from django.db.models import Q
from .userManagement import *
from main.msgUtil import *

def groups(request):
    if request.user.is_superuser == False:
        return HttpResponseRedirect(reverse('main:home'))
    return render(request, 'admin/groups.html',{'form' : CreateGroup(), "groups":getGroups(request)})

def deleteGroup(request, group_id):
    Group.objects.filter(lecturer=request.user).filter(id=group_id).delete()
    return render(request, 'admin/groups.html',{'form' : CreateGroup(), "groups":getGroups(request)})

def deleteFromGroup(request,student_id):
    student = User.objects.filter(id=student_id).first()
    studentGroup =  StudentGroup.objects.filter(student=student).first()
    group = Group.objects.filter(id=studentGroup.group.id).first()
    studentGroup.delete()
    return groupDetails(request, group.id)

def responses(request):
    activeOverlap = "responses"
    lecturer = User.objects.filter(id=request.user.id).first()
    return render(request, 'admin/responses.html',{'answers': getAllNotRatedAnswers(lecturer), 'activeOverlap': activeOverlap})

def responseDetails(request,answer_id):
    activeOverlap = "responses"
    lecturer = User.objects.filter(id=request.user.id).first()
    return render(request, 'admin/responseDetails.html',{
        'answer': getDataAboutAnswer(answer_id, lecturer)[0],
        'medals': getAllMedals(),
        'activeOverlap': activeOverlap})

def students(request):
    activeOverlap = "students"
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        index_nr = request.POST.get('index_nr')
        msg = createUser(first_name, last_name, index_nr)
        return render(request, 'admin/students.html',{'students':getStudentsList(), 'message':msg})
    return render(request, 'admin/students.html',{'students':getStudentsList(), 'activeOverlap': activeOverlap})

def addStudent(request):
    activeOverlap = "students"
    return render(request, 'admin/addStudent.html', {'activeOverlap': activeOverlap})

def deleteStudent(request, student_id):
    activeOverlap = "students"
    User.objects.filter(is_superuser=False).filter(id=student_id).delete()
    return render(request, 'admin/students.html',{'students':getStudentsList(), 'activeOverlap': activeOverlap})

def editStudent(request,student_id):
    return render(request, 'admin/studentDetails.html',
        {
            'student':getStudentDetails(student_id),
            'stages': getStudentStages(student_id)
        })

def excercises(request):
    activeOverlap = "excercises"
    return render(request, 'admin/excercises.html', {'activeOverlap': activeOverlap})

def excercisesWithTasks(request,stage_id):
    activeOverlap = "excercises"
    stage = Stage.objects.filter(id = stage_id).first()
    tasks = getAllTaskByStage(stage)
    return render(request,'admin/excercises.html',{'tasks': tasks, 'stageId':stage_id, 'activeOverlap': activeOverlap})

def getAllTaskByStage(stage):
    tasks = StageTasks.objects.filter(stage = stage)
    result =[]
    for task in tasks:
        difficulty_level = DifficultyLevel.objects.filter(id=task.difficulty_level.id).first()
        result.append({
            'title' : difficulty_level.title,
            'level' : difficulty_level.level,
            'id' : task.id,
        })
    return result

def excerciseDetails(request,task_id):
    activeOverlap = "excercises"
    task = StageTasks.objects.filter(id=task_id).first()
    stage = Stage.objects.filter(id=task.stage.id).first()
    if request.method == 'POST':
        task_content = request.POST.get("task_content")
        prompt = request.POST.get('prompt')
        points = request.POST.get("points")
        sampleAnswer = request.POST.get("sampleAnswer")
        difficulty_level_post = request.POST.get('difficulty_level')
        difficulty_level = DifficultyLevel.objects.filter(level = difficulty_level_post).first()
        task.description = task_content
        task.points = points
        task.exp_points = points
        task.sampleAnswer = sampleAnswer
        task.prompt = prompt
        task.difficulty_level = difficulty_level
        task.save()
    task = StageTasks.objects.filter(id=task_id).first()
    difficulty_level = DifficultyLevel.objects.filter(id=task.difficulty_level.id).first()
    
    result = {
        'stage_name' : stage.name,
        'stage_id' : stage.id,
        'difficulty_name' : difficulty_level.title,
        'difficulty_level' : difficulty_level.level,
        'difficulty_id':difficulty_level.id,
        'task_content' : task.description,
        'prompt' : task.prompt,
        'points' : task.points,
        'task_id' : task.id,
        'sample_answer': task.sampleAnswer
    }
    return render(request, 'admin/excerciseDetails.html',{'task': result, 'range': range(5), 'activeOverlap': activeOverlap })


def newExcercise(request,stage_id):
    activeOverlap = "excercises"
    stage = Stage.objects.filter(id=stage_id).first()
    if request.method == "POST":
        task_content = request.POST.get("task_content")
        prompt = request.POST.get('prompt')
        points = request.POST.get("points")
        sampleAnswer = request.POST.get("sampleAnswer")
        difficulty_level_post = request.POST.get('difficulty_level')
        difficulty_level = DifficultyLevel.objects.filter(level = difficulty_level_post).first()
        StageTasks.objects.create(
            stage = stage,
            description = task_content,
            points = points,
            exp_points = points,
            sampleAnswer = sampleAnswer,
            prompt = prompt,
            difficulty_level = difficulty_level
        )
        return excercisesWithTasks(request,stage_id)
    if request.method == 'GET':
        return render(request, 'admin/newExcercise.html',{
            'stage_id' : stage_id,
            'stage_name': stage.name,
            'range': range(5),
            'activeOverlap': activeOverlap
        })
    

def deleteExcercise(request, stage_id, task_id):
    stage = Stage.objects.filter(id=stage_id).first()
    task = StageTasks.objects.filter(stage=stage).filter(id=task_id).first()
    if task != None:
        task.delete()
    return excercisesWithTasks(request,stage_id)

def challenges(request):
    activeOverlap = "challenges"
    return render(request, 'admin/challenges.html', {'activeOverlap': activeOverlap})

def groupDetails(request, group_id):
    students = getGroupDetails(group_id)
    students_without_group = getStudentsWithoutGroup()
    stages = getStages()
    return render(request, 'admin/groupDetails.html',{'students':students,'group_id':group_id, 'students_without_group': students_without_group, 'stages':stages})

def messages(request):
    activeOverlap = "messages"
    user = User.objects.filter(id=request.user.id).first()
    msgs = getAllUserMessages(user)
    return render(request, 'admin/messages.html',{'messages':msgs, 'activeOverlap': activeOverlap})

def sendMessage(request, message_id):
    activeOverlap = "messages"
    msg = getMessageDetails(message_id,request.user)
    return render(request, 'admin/sendMessage.html', {
        'activeOverlap': activeOverlap,
        'message': msg
    })

def newMessage(request):
    activeOverlap = "messages"
    return render(request, 'admin/sendMessage.html', {
        'activeOverlap': activeOverlap,
        'receivers' : getAllReceiver(request.user)
        })

def readMessage(request,message_id):
    activeOverlap = "messages"
    return render(request, 'admin/readMessage.html', {
        'activeOverlap': activeOverlap,
        'message':getMessageDetails(message_id,request.user)
    })

def addStudentToGroup(request,group_id):
    student_id = request.POST.get('student_id')
    student = User.objects.filter(id=student_id).first()
    group = Group.objects.filter(id=group_id).first()
    studentGroup = StudentGroup.objects.filter(student=student).first()
    if studentGroup == None:
        StudentGroup.objects.create(group=group,student=student)
    else :
        studentGroup.group = group
        studentGroup.save()
    return groupDetails(request, group_id)
    
def addGroup(request):
    if request.method == "POST":
        sid = transaction.savepoint()
        form = CreateGroup(request.POST, request.FILES)
        if form.is_valid():
            filepath = request.FILES['groupFile'] if 'groupFile' in request.FILES else False
            if filepath != False:
                file_in_memory = request.FILES['groupFile'].read()
                group = Group.objects.create(name=request.POST.get('groupName'),lecturer=request.user)
                
                is_created = createUsersFromWorkbook(file_in_memory, group)
                if is_created == False:
                    transaction.savepoint_rollback(sid)
                    Group.objects.filter(id=group.id).first().delete()
                else :
                    transaction.savepoint_commit(sid)
                return render(request, 'admin/groups.html',{'groups':getGroups(request),'form' : CreateGroup(),'message':is_created})
            else :
                group = Group.objects.create(name=request.POST.get('groupName'),lecturer=request.user)
                return render(request, 'admin/groups.html',{'groups':getGroups(request),'form' : CreateGroup(),'message':True})
    return render(request, 'admin/groups.html',{'groups':getGroups(request),'form' : CreateGroup()})

def getStudentsList():
    students = User.objects.filter(is_superuser = False)
    return students

def getStages():
    stages = Stage.objects.filter()
    return stages

def getGroupDetails(group_id):
    students = []
    group = Group.objects.filter(id=group_id).first()
    studentsGroup = StudentGroup.objects.filter(group=group)
    for stg in studentsGroup:
        st = User.objects.filter(id=stg.student.id).first()
        stDetails = AccountDetails.objects.filter(user=st).first()
        students.append({
            'id':st.id,
            'first_name': st.first_name,
            'last_name' : st.last_name,
            'username' : st.username,
            'email' : st.email,
            'points' : stDetails.points
        })
    students = sorted(students, key=lambda k: k.get('points'),reverse = True)
    return students

def getGroups(request):
    user = request.user
    groups = Group.objects.filter(lecturer=user)
    return groups


def getStudentDetails(student_id):
    user = User.objects.filter(id=student_id).first()
    group = None
    if StudentGroup.objects.filter(student=user).exists():
        studentGroup = StudentGroup.objects.filter(student=user).first()
        group = Group.objects.filter(id=studentGroup.group.id).first()
    accountDetails = AccountDetails.objects.filter(user=user).first()
    index_number = str(user.username[1:])
    details = {
        'id' : user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'index_number': index_number,
        'group': group,
        'level': accountDetails.level,
        'current_hp': accountDetails.current_hp,
        'current_exp': accountDetails.current_exp,
        'max_exp': accountDetails.exp_max,
        'points': accountDetails.points
    }
    return details

def getStudentTaksForStage(stage_id, student_id):
    student = User.objects.filter(id=student_id).first()
    stage = Stage.objects.filter(id=stage_id)
    studentStage = StageStudent.objects.filter(stage = stage).filter(student=student).first()
    tasks = Answer.objects.filter()

def getStudentStages(student_id):
    user = User.objects.filter(id=student_id).first()
    studentStage = StageStudent.objects.filter(student=user)
    stageDetails = []
    for stageStudent in studentStage:
        stage = Stage.objects.filter(id=stageStudent.stage.id).first()
        answers = Answer.objects.filter(stageStudent=stageStudent)
        answerDetails = []
        for answer in answers:
            task = StageTasks.objects.filter(id=answer.task.id).first()
            difficultyLevel = DifficultyLevel.objects.filter(id=task.difficulty_level.id).first()
            answerDetails.append({
                "task_id" : task.id,
                "answer_id": answer.id,
                "completed" : answer.completed,
                "rated": answer.rated,
                "note": answer.note,
                "difficulty_level_id": difficultyLevel.id,
                "title" : difficultyLevel.title
            })
        stageDetails.append({
            "id": stage.id,
            "name": stage.name,
            "tasks": answerDetails
        })
    return stageDetails

def getDataAboutAnswer(answer_id, lecturer):
    answer = Answer.objects.filter(id=answer_id).first()
    stageStudent = StageStudent.objects.filter(id=answer.stageStudent.id).first()
    student = User.objects.filter(id=stageStudent.student.id).first()
    task = StageTasks.objects.filter(id=answer.task.id).first()
    difficultyLevel = DifficultyLevel.objects.filter(id=task.difficulty_level.id).first()
    stage = Stage.objects.filter(id=task.stage.id).first()
    studentGroup = StudentGroup.objects.filter(student = student).first()
    group = Group.objects.filter(id=studentGroup.group.id).filter(lecturer=lecturer).first()
    response = []
    if(group == None ):
        return response
    minus_points = 0
    if answer.usedPrompt == 1:
        minus_points = task.points * 0.2
    max_points_to_gain = task.points - minus_points
    response.append({
        "task_description": task.description,
        "answer": answer.answerSql,
        "answer_id": answer_id,
        "usedPrompt": answer.usedPrompt,
        "note": answer.note,
        "rated": answer.rated,
        "completed_at":answer.completed_at,
        "group_id": group.id, 
        "group_name": group.name,
        "student_id": student.id,
        "student_firstname": student.first_name,
        "student_lastname": student.last_name,
        "max_task_points" : task.points,
        "max_points_to_gain": max_points_to_gain,
        "point_scale": range(int(max_points_to_gain))
    })
    return response

def getAllMedals():
    medalsObjects = Achievement.objects.all().order_by('id')
    result = []
    for medal in medalsObjects:
        result.append({
            "id" : medal.id,
            "name" : medal.name,
            "points" : medal.points,
            "description" : medal.description,
            "picture": medal.picture
        })
    return result

def rateAnswer(request):
    if request.method == 'POST':
        print(request.POST)
    return responses(request)

def getAllLecturerStudents(lecturer):
    students =[]
    groups = Group.objects.filter(lecturer=lecturer)
    if groups.count() == 0 or groups == None:
        return students
    for group in groups:
        studentsGroup = StudentGroup.objects.filter(group=group)
        if studentsGroup != None:
            for studentGroup in studentsGroup:
                students.append(User.objects.filter(id=studentGroup.student.id).first())
    
    return students

def getIdList(objs):
    lista = []
    for obj in objs:
        lista.append(obj.id)
    return lista

def getAllNotRatedAnswers(lecturer):
    results =[]
    students = getAllLecturerStudents(lecturer)
    if students != None :
        for student in students:
            stageStudentList = StageStudent.objects.filter(student=student)
            group = getStudentGroup(student)
            if stageStudentList != None:
                for stageStudent in stageStudentList:
                    answers = Answer.objects.filter(stageStudent=stageStudent).filter(rated = 0).filter(completed=1)
                    if answers != None :
                        for answer in answers:
                            results.append({
                                'id' : answer.id,
                                'student_id':student.id,
                                'student' : student.first_name + ' ' + student.last_name,
                                'group_id': group.id,
                                'group_name': group.name,
                                'date': answer.completed_at
                            })
    return results

def getStudentGroup(student):
    studentGroup = StudentGroup.objects.filter(student=student).first()
    group = Group.objects.filter(id=studentGroup.group.id).first()
    return group

def getStudentsWithoutGroup():
    results = []
    students = User.objects.filter(is_superuser = 0)
    for student in students:
        if not StudentGroup.objects.filter(student=student).exists():
            results.append({
                'student_id' : student.id ,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'username' : student.username[1:]
            })
    return results

def getAllUserMessages(user):
    result = []
    messagesAnswerList = MessagesAnswer.objects.all()
    messagesAnswerIdList = []
    for messageAnswer in messagesAnswerList:
        messagesAnswerIdList.append(messageAnswer.message.id)
    msgs = Messages.objects.filter(Q(from_user=user) | Q(to_user=user)).exclude(id__in=messagesAnswerIdList)
    for msg in msgs:
        from_user = User.objects.filter(id=msg.from_user.id).first()
        is_read = msg.is_read
        if MessagesAnswer.objects.filter(answer_to=msg).exists():
            tempMsgA = MessagesAnswer.objects.filter(answer_to=msg).last()
            last_msg = Messages.objects.filter(id=tempMsgA.message.id).first()
            is_read = last_msg.is_read
        result.append({
            "id": msg.id,
            "from_user_id": from_user.id,
            "from_user_name" : from_user.first_name + " "+ from_user.last_name,
            "title" : msg.title,
            "date": msg.send_date,
            "is_read": is_read 
        }) 
    return result