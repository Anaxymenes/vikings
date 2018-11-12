from django.contrib.auth.hashers import make_password, check_password
from models.models import *
from io import BytesIO
from openpyxl import load_workbook, workbook, cell
from .forms import CreateGroup
from django.contrib.auth.models import User
from django.db import transaction
import operator
from django.db.models import Q
from main.stageManagement import createNewStudentStages

def createStudentFromWorkbook(file_in_memory, group):
    try:
        wb = load_workbook(filename=BytesIO(file_in_memory))
        for sheetname in wb.sheetnames:
            rows = wb[sheetname].max_row
            columns = wb[sheetname].max_column
            ws = wb[sheetname]
            firstname_index = 2
            lastname_index = 3
            index_number_index = 4
            for i in range(1,columns+1):
                cell_value = ws.cell(row=1,column=i).value
                if cell_value == "Imię" or cell_value == "Firstname":
                    firstname_index = i
                elif cell_value == "Nazwisko" or cell_value == "Lastname":
                    lastname_index = i
                elif cell_value == "Numer Indeksu" or cell_value == "Index" or cell_value == "Nr_Indeksu":
                    index_number_index = i
            for i in range (2, rows+1):
                password = ws.cell(row=i,column=firstname_index).value [:3]
                password += ws.cell(row=i,column=lastname_index).value [:3]
                password += str(ws.cell(row=i,column=index_number_index).value) [-3:]
                username = 's'+str(ws.cell(row=i,column=index_number_index).value)
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username,None,password)
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

def createStudent(first_name, last_name, index_nr):
    try:
        password = first_name[:3] + last_name[:3] + str(index_nr)[:3]
        username = 's'+str(index_nr)
        if User.objects.filter(username=username).exists():
            return False
        user = User.objects.create_user(username=username,password=password, first_name=first_name, last_name=last_name)
        accountDetails = AccountDetails.objects.create(
            user=user,
            level=0,
        )
        createNewStudentStages(user)
        return True
    except:
        return False

def getUser(user_id):
    if User.objects.filter(id=user_id).exists():
        return User.objects.filter(id=user_id).first()