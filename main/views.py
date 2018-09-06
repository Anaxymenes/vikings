<<<<<<< HEAD
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html', {})

def lesson(request):
    return render(request, 'main/lesson.html', {})

def playerProfile(request):
    return render(request, 'main/playerProfile.html', {})

=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 32c13168b4c1411ffbbea49a39c3ec3432969980
