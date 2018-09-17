from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from models.models import AccountDetails, Stage


def index(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html', {})
    return HttpResponseRedirect(reverse('login:login'))

def lesson(request,stage_id):
    stage = Stage.objects.filter(id=stage_id).first()
    return render(request, 'main/lesson.html', {
        "stage":stage
    })

def playerProfile(request):
    return render(request, 'main/playerProfile.html', {})

