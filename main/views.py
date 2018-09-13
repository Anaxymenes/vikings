from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    player="Mateusz Bogacki"
    level=4
    levels = range(1, level + 1)
    return render(request, 'main/index.html', {"player": player, "levels": levels})

def lesson(request):
    return render(request, 'main/lesson.html', {})

def playerProfile(request):
    return render(request, 'main/playerProfile.html', {})

