from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

def index(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)
        print(user)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('main:home'))
        else :
            return render(request, 'login/index.html', {'message' : 'Login lub hasło są nieprawidłowe'})
    return render(request, 'login/index.html', {})

def register(request):
    return render(request, 'login/register.html', {})

def changePassword(request):
    return render(request, 'login/changePassword.html', {})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))