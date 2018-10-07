from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from models.models import StudentGroup
from io import BytesIO
from openpyxl import load_workbook, workbook, cell
from .forms import CreateGroup
from django.contrib.auth.models import User

def groups(request):
    return render(request, 'admin/groups.html',{'form' : CreateGroup()})

def responses(request):
    return render(request, 'admin/responses.html')

def excercises(request):
    return render(request, 'admin/excercises.html')

def challenges(request):
    return render(request, 'admin/challenges.html')

def groupDetails(request):
    return render(request, 'admin/groupDetails.html')

def addGroup(request):
    if request.method == "POST":
        print(request.POST)
        form = CreateGroup(request.POST, request.FILES)
        if form.is_valid():
            file_in_memory = request.FILES['groupFile'].read()
            wb = load_workbook(filename=BytesIO(file_in_memory))
            print(wb.sheetnames)
            for sheetname in wb.sheetnames:
                rows = wb[sheetname].max_row
                columns = wb[sheetname].max_column
                ws = wb[sheetname]
                firstname_index = 1
                lastname_index = 1
                pesel_index = 1
                index_number_index = 1
                email_index = 1
                for i in range(1,columns+1):
                    cell_value = ws.cell(row=1,column=i).value
                    if cell_value == "Imię" or cell_value == "Firstname":
                        firstname_index = i
                    elif cell_value == "Nazwisko" or cell_value == "Lastname":
                        lastname_index = i
                    elif cell_value == "PESEL":
                        pesel_index = i
                    elif cell_value == "Numer Indeksu" or cell_value == "Index":
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
                    
            return render(request, 'admin/excercises.html')
    return render(request, 'admin/groups.html',{'form' : CreateGroup()})
