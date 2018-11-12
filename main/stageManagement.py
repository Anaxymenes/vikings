from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

def openStages(user):
    openStages = []
    accDet = AccountDetails.objects.filter(user=user).first()
    if accDet.level == 0:
        return openStages
    max_level = accDet.level
    for x in range(1,max_level):
        stage = Stage.objects.filter(id=x).first()
        if StageStudent.objects.filter(student=user).filter(complete=0).filter(stage=stage).exists() :
            openStages.append(stage.id)
    return openStages

def createNewStudentStages(student):
    index = 0
    for stage in Stage.objects.all():
        start_at =  timezone.now() + (index * timedelta(days=7))
        end_at = timezone.now() + (index * timedelta(days=7)) + timedelta(days=7)
        StageStudent.objects.create(
            stage = stage,
            student = student,
            databaseSql = "Not implemented yet",
            complete = False,
            start_at = start_at,
            end_at = end_at 
        )
        index += 1
    return True

def clearAllStudentStage(student):
    if StageStudent.objects.filter(student=student).exists():
        StageStudent.objects.filter(student=student).delete()

def updateStageStatus():
    stageStudents = StageStudent.objects.all()
    current_date = timezone.now()
    for stageStudent in stageStudents:
        if stageStudent .to_open and stageStudent.to_close == False:
            stageStudent.complete = 0
            print(updateLevel(stageStudent.student,stageStudent.stage.id))
        if stageStudent.to_close:
            stageStudent.complete = 1
        stageStudent.save()
    return True

def updateLevel(student, stage_level):
    accDet = AccountDetails.objects.filter(user=student).first()
    if accDet.level < stage_level :
        accDet.level = stage_level
        accDet.save()
    return True