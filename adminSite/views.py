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

def groups(request):
    if request.user.is_superuser == False:
        return HttpResponseRedirect(reverse('main:home'))
    return render(request, 'admin/groups.html',{'form' : CreateGroup(), "groups":getGroups(request)})

def deleteGroup(request, group_id):
    Group.objects.filter(lecturer=request.user).filter(id=group_id).delete()
    return render(request, 'admin/groups.html',{'form' : CreateGroup(), "groups":getGroups(request)})

def responses(request):
    return render(request, 'admin/responses.html')

def responseDetails(request):
    return render(request, 'admin/responseDetails.html')

def students(request):
    return render(request, 'admin/students.html',{'students':getStudentsList()})

def deleteStudent(request, student_id):
    User.objects.filter(is_superuser=False).filter(id=student_id).delete()
    return render(request, 'admin/students.html',{'students':getStudentsList()})

def editStudent(request,student_id):
    print(getStudentDetails(student_id))
    return render(request, 'admin/studentDetails.html',{'student':getStudentDetails(student_id)})

def excercises(request):
    return render(request, 'admin/excercises.html')

def excercisesWithTasks(request,stage_id):
    stage = Stage.objects.filter(id = stage_id).first()
    tasks = getAllTaskByStage(stage)
    return render(request,'admin/excercises.html',{'tasks': tasks, 'stageId':stage_id})

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
    return render(request, 'admin/excerciseDetails.html',{'task': result, 'range': range(5)})


def newExcercise(request,stage_id):
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
            'range': range(5)
        })
    

def deleteExcercise(request, stage_id, task_id):
    stage = Stage.objects.filter(id=stage_id).first()
    task = StageTasks.objects.filter(stage=stage).filter(id=task_id).first()
    if task != None:
        task.delete()
    return excercisesWithTasks(request,stage_id)

def challenges(request):
    return render(request, 'admin/challenges.html')

def groupDetails(request, group_id):
    students = getGroupDetails(group_id)
    print(students)
    return render(request, 'admin/groupDetails.html',{'students':students})

def messages(request):
    return render(request, 'admin/messages.html')

def addGroup(request):
    if request.method == "POST":
        sid = transaction.savepoint()
        print(request.POST)
        form = CreateGroup(request.POST, request.FILES)
        if form.is_valid():
            file_in_memory = request.FILES['groupFile'].read()
            group = Group.objects.create(name=request.POST.get('groupName'),lecturer=request.user)
            
            is_created = createUsersFromWorkbook(file_in_memory, group)
            if is_created == False:
                transaction.savepoint_rollback(sid)
                Group.objects.filter(id=group.id).first().delete()
            else :
                transaction.savepoint_commit(sid)
            return render(request, 'admin/groups.html',{'groups':getGroups(request),'form' : CreateGroup(),'message':is_created})
    return render(request, 'admin/groups.html',{'groups':getGroups(request),'form' : CreateGroup()})

def getStudentsList():
    students = User.objects.filter(is_superuser = False)
    return students

def getGroupDetails(group_id):
    students = []
    group = Group.objects.filter(id=group_id).first()
    studentsGroup = StudentGroup.objects.filter(group=group)
    for stg in studentsGroup:
        st = User.objects.filter(id=stg.student.id).first()
        stDetails = AccountDetails.objects.filter(user=st).first()
        students.append({
            'first_name': st.first_name,
            'last_name' : st.last_name,
            'username' : st.username,
            'email' : st.email,
            'points' : stDetails.points
        })
        print(st)
    students = sorted(students, key=lambda k: k.get('points'),reverse = True)
    return students

def getGroups(request):
    user = request.user
    groups = Group.objects.filter(lecturer=user)
    return groups

def createUsersFromWorkbook(file_in_memory, group):
    try:
        wb = load_workbook(filename=BytesIO(file_in_memory))
        for sheetname in wb.sheetnames:
            rows = wb[sheetname].max_row
            columns = wb[sheetname].max_column
            ws = wb[sheetname]
            firstname_index = 2
            lastname_index = 3
            pesel_index = 4
            index_number_index = 5
            email_index = 6
            for i in range(1,columns+1):
                cell_value = ws.cell(row=1,column=i).value
                if cell_value == "Imię" or cell_value == "Firstname":
                    firstname_index = i
                elif cell_value == "Nazwisko" or cell_value == "Lastname":
                    lastname_index = i
                elif cell_value == "PESEL":
                    pesel_index = i
                elif cell_value == "Numer Indeksu" or cell_value == "Index" or cell_value == "Nr_Indeksu":
                    index_number_index = i
                elif cell_value == "E-mail" or cell_value == "Email":
                    email_index = i
            for i in range (2, rows+1):
                password = ws.cell(row=i,column=firstname_index).value [:3]
                password += ws.cell(row=i,column=lastname_index).value [:3]
                password += str(ws.cell(row=i,column=pesel_index).value) [-3:]

                username = 's'+str(ws.cell(row=i,column=index_number_index).value)
                email = str(ws.cell(row=i,column=email_index).value)
                print(password)
                user = User.objects.create_user(username,email,password)
                user.first_name = ws.cell(row=i,column=firstname_index).value
                user.last_name = ws.cell(row=i,column=lastname_index).value 
                user.save()
                studentGroup = StudentGroup.objects.create(group=group, student=user)
                studentGroup.save()
                accountDetails = AccountDetails.objects.create(hp_max=100,current_hp=100,level=0,points=0,exp_max=100,current_exp=0,user=user)
                accountDetails.save()
        return True
    except:
        return False

def getStudentDetails(student_id):
    user = User.objects.filter(id=student_id).first()
    studentGroup = StudentGroup.objects.filter(student=user).first()
    group = Group.objects.filter(id=studentGroup.group.id).first()
    print(group.name)
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
