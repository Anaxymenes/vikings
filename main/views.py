from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User

player="Mateusz Bogacki"

def index(request):
    if request.user.is_authenticated:
        level=4
        levels = range(1, level + 1)
        return render(request, 'main/index.html', {"player": request.user.get_full_name(), "levels": levels})
    return HttpResponseRedirect(reverse('login:login'))

def lesson(request):
    return render(request, 'main/lesson.html', {"player": player})

def playerProfile(request):
    return render(request, 'main/playerProfile.html', {"player": player,})

