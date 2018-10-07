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
                for i in range (1, rows+1):
                    for j in range(1,columns+1):
                        cell_obj=ws.cell(row=i,column=j)
                        print(cell_obj.value, end =' | ')
            return render(request, 'admin/excercises.html')
    return render(request, 'admin/groups.html',{'form' : CreateGroup()})
