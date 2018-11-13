from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from main.stageManagement import *

def getGroupByIdShortDetails(group_id):
    return Group.objects.filter(id=group_id).first()

def replaceStringInDate(date) :
    date_change = date.replace("T"," ")
    return date_change

def udpateStageStudentDates(student, stage, lista):
    updateLessonDate(student,stage,replaceStringInDate(lista['min_date']),replaceStringInDate(lista['max_date']))
    updateStageStatus()

def updateGroupDates(group, lista):
    studentsGroup = StudentGroup.objects.filter(group=group)
    for i in range(1,6):
        #print("Min value => " +lista["min_"+str(i)])
        stage = Stage.objects.filter(id=i).first()
        for studentGroup in studentsGroup:
            updateLessonDate(studentGroup.student,
                stage,
                replaceStringInDate(lista["min_"+str(i)]),
                replaceStringInDate(lista["max_"+str(i)])
             )
    updateStageStatus()
    return True
    