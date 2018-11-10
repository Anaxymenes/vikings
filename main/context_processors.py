from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta, timezone
from .msgUtil import isNewMessages
from .stageManagement import *

def add_variable_to_context(request):
    if request.user.is_authenticated and request.user.is_superuser == False: 
        accountDetails = AccountDetails.objects.filter(user=request.user).first()
        level = accountDetails.level
        levels = range(1, level + 1)
        global_ranking = global_rank(request.user)
        group_ranking = group_rank(request.user)
        openLevels = openStages(request.user)
        exp_bar = (accountDetails.current_exp * 100) / accountDetails.exp_max
        hp_bar = (accountDetails.current_hp * 100) / accountDetails.hp_max
        return {
            "player": request.user.get_full_name(), 
            "levels": levels, 
            "openLevels": openLevels,
            "account": accountDetails,
            "exp_bar": exp_bar,
            "hp_bar": hp_bar,
            "new_msg": isNewMessages(request.user),
            "global_rank": global_ranking,
            "group_rank": group_ranking
            }
    elif request.user.is_authenticated and request.user.is_superuser :
        return {
            "new_msg": isNewMessages(request.user)
        }
    else :
        return {}

def start_stages(request):
    stages = StageStudent.objects.all()
    current_date = datetime.now()
    for stage in stages:
        if stage.end_at >= current_date:
            stage.complete = 1
            stage.save()

def global_rank(user):
    studentsSortedByPoints = sorted(AccountDetails.objects.all(), key=lambda student: student.points, reverse=True)
    studentRank = studentsSortedByPoints.index(AccountDetails.objects.filter(user = user).first()) + 1
    return studentRank 

def group_rank(user):
    groupMates = StudentGroup.objects.filter(group = StudentGroup.objects.filter(student = user).first().group.id)
    groupStudents = []
    for mate in groupMates:
        groupStudents.append(AccountDetails.objects.filter(user = mate.student).first())
    groupStudentsSortedByPoints = sorted(groupStudents, key=lambda student: student.points, reverse=True)
    studentRank = groupStudentsSortedByPoints.index(AccountDetails.objects.filter(user = user).first()) + 1
    return studentRank