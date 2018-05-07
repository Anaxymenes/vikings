from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'login/index.html',{})

def register(request):
    return render(request,'login/register.html',{})

def changePassword(request):
    return render(request, 'login/changePassword.html',{})