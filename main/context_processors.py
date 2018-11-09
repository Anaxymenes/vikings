from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta, timezone
from .msgUtil import isNewMessages

def add_variable_to_context(request):
    if request.user.is_authenticated and request.user.is_superuser == False: 
        accountDetails = AccountDetails.objects.filter(user=request.user).first()
        level = accountDetails.level
        levels = range(1, level + 1)
        exp_bar = (accountDetails.current_exp * 100) / accountDetails.exp_max
        hp_bar = (accountDetails.current_hp * 100) / accountDetails.hp_max
        print(isNewMessages(request.user))
        return {
            "player": request.user.get_full_name(), 
            "levels": levels, 
            "account": accountDetails,
            "exp_bar": exp_bar,
            "hp_bar": hp_bar,
            "new_msg": isNewMessages(request.user)
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