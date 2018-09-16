from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

def adminSite(request):
    return render(request, 'admin/groups.html')
