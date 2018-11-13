from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from main.stageManagement import *

def createAbsenceList(user):
    for i in range(1,6):
        UserAbsence.objects.create(
            absence = False,
            student = user,
            lesson_nr = i,
            absence_date = None
        )
    return True

def getStudentAbsence(student):
    results = []
    usrAbs = UserAbsence.objects.filter(student=student)
    for userAbsence in usrAbs:
        results.append({
            "absence": userAbsence.absence,
            "lesson": userAbsence.lesson_nr,
            "id" : userAbsence.id,
            "date" : userAbsence.absence_date
        })
    return results