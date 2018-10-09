from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.hashers import make_password, check_password
from models.models import StudentGroup, Group, AccountDetails
from io import BytesIO
from openpyxl import load_workbook, workbook, cell
from .forms import CreateGroup
from django.contrib.auth.models import User

def groups(request):
    if request.user.is_superuser == False:
        return HttpResponseRedirect(reverse('main:home'))
    return render(request, 'admin/groups.html',{'form' : CreateGroup(), "groups":getGroups(request)})

def deleteGroup(request, group_id):
    Group.objects.filter(lecturer=request.user).filter(id=group_id).delete()
    return render(request, 'admin/groups.html',{'form' : CreateGroup(), "groups":getGroups(request)})

def responses(request):
    return render(request, 'admin/responses.html')

def students(request):
    return render(request, 'admin/students.html',{'students':getStudentsList()})

def deleteStudent(request, student_id):
    User.objects.filter(is_superuser=False).filter(id=student_id).delete()
    return render(request, 'admin/students.html',{'students':getStudentsList()})

def editStudent(request,student_id):
    return render(request, 'admin/studentDetails.html',{'student':getStudentDetails(student_id)})

def excercises(request):
    return render(request, 'admin/excercises.html')

def excerciseDetails(request):
    return render(request, 'admin/excerciseDetails.html')

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
        print(request.POST)
        form = CreateGroup(request.POST, request.FILES)
        if form.is_valid():
            file_in_memory = request.FILES['groupFile'].read()
            group = Group.objects.create(name=request.POST.get('groupName'),lecturer=request.user)
            group.save()
            is_created = createUsersFromWorkbook(file_in_memory, group)
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
        students.append(st)
        print(st)
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
    accountDetails = AccountDetails.objects.filter(user=user)
    index_number = str(user.username[1:])
    details = {
        'id' : user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'index_number': index_number,
        'current_group': group.name,
        'level': accountDetails.level,
        'current_hp': accountDetails.current_hp,
        'current_exp': accountDetails.current_exp,
        'max_exp': accountDetails.exp_max,
        'points': accountDetails.points
    }
    return details
