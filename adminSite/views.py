from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

def groups(request):
    return render(request, 'admin/groups.html')

def responses(request):
    return render(request, 'admin/responses.html')

def excercises(request):
    return render(request, 'admin/excercises.html')

def challenges(request):
    return render(request, 'admin/challenges.html')

def groupDetails(request):
    return render(request, 'admin/groupDetails.html')

