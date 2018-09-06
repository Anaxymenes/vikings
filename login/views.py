from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    #passws = make_password("Admin3323")
    existPasswd = "pbkdf2_sha256$100000$KMed1wMNdRa1$jTpKWdvFt/hxF203dpNBqqK235BWyedOLsherXp+pEY="
    passws = check_password("Admin3323", existPasswd)
    return render(request, 'login/index.html', {'password': passws,})

def register(request):
    return render(request, 'login/register.html', {})

def changePassword(request):
    return render(request, 'login/changePassword.html', {})