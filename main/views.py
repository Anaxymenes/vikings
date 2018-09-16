from django.http import HttpResponse
from django.shortcuts import render


player="Mateusz Bogacki"

def index(request):
    level=4
    levels = range(1, level + 1)
    return render(request, 'main/index.html', {"player": player, "levels": levels})

def lesson(request):
    return render(request, 'main/lesson.html', {"player": player})

def playerProfile(request):
    return render(request, 'main/playerProfile.html', {"player": player,})

