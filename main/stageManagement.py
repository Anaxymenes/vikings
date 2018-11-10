from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta, timezone
from django.db import transaction
from django.db.models import Q

def openStages(user):
    openStages = []
    stageStudent = StageStudent.objects.filter(student = user).filter(complete = 0)
    for i in stageStudent:
        openStages.append({
            "openLevel": i.stage.id
        }) 
        print(i.stage.id)
    return openStages