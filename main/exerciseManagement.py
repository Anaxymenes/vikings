from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from models.models import *
import logging
from datetime import datetime, timedelta
from .msgUtil import *

def saveCloseExcercise(user_id,stage_id, answer_id, answerSql, usedPrompt, close):
    student = User.objects.filter(id=user_id).first()
    stage = Stage.objects.filter(id=stage_id).first()
    stageStudent = StageStudent.objects.filter(student=student).filter(stage=stage).first()
    answer = Answer.objects.filter(id=answer_id).filter(stageStudent=stageStudent).first()
    answer.answerSql = answerSql
    answer.usedPrompt = usedPrompt
    if close :
        answer.completed = 1
        answer.completed_at = datetime.now()
    answer.save()

