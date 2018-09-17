from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from models.models import AccountDetails

player="Mateusz Bogacki"

def index(request):
    if request.user.is_authenticated:
        accountDetails = AccountDetails.objects.filter(user=request.user).first()
        level = accountDetails.level
        levels = range(1, level + 1)
        exp_bar = (accountDetails.current_exp * 100) / accountDetails.exp_max
        hp_bar = (accountDetails.current_hp * 100) / accountDetails.hp_max
        return render(request, 'main/index.html', {
            "player": request.user.get_full_name(), 
            "levels": levels, 
            "account": accountDetails,
            "exp_bar": exp_bar,
            "hp_bar": hp_bar
            })
    return HttpResponseRedirect(reverse('login:login'))

def lesson(request):
    return render(request, 'main/lesson.html', {"player": player})

def playerProfile(request):
    return render(request, 'main/playerProfile.html', {"player": player,})

