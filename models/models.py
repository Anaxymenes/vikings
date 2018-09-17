from django.db import models
from django.contrib.auth.models import User

class AccountDetails(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    hp_max = models.IntegerField(default=100)
    current_hp = models.IntegerField(default=100)
    level = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    exp_max = models.IntegerField(default=100)
    current_exp = models.IntegerField(default=0)
    
class Achievement(models.Model):
    name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=200)

class Stage(models.Model):
    name = models.CharField(max_length=50)

class Task(models.Model):
    stageTaskId = models.ForeignKey(Stage, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2500)
    points = models.IntegerField(default=4)
    sampleAnswer = models.CharField(max_length=2500)

class AchievementTask(models.Model):
    achievementId = models.ForeignKey(Achievement, on_delete = models.PROTECT)
    taskId = models.ForeignKey(Task, on_delete=models.CASCADE)
    studentID = models.ForeignKey(User, on_delete=models.CASCADE)

class Answer(models.Model):
    studentId = models.ForeignKey(User, on_delete = models.CASCADE)
    taskID = models.ForeignKey(Task, on_delete=models.PROTECT)
    answerSql = models.CharField(max_length=2500)

class StageStudent(models.Model):
    stageId = models.ForeignKey(Stage, on_delete=models.PROTECT)
    studentID = models.ForeignKey(User, on_delete=models.CASCADE)
    databaseSql = models.CharField(max_length=5000)
    complete = models.BooleanField(default=0)

class StageTasks(models.Model):
    stageId = models.ForeignKey(Stage, on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    title = models.CharField(max_length=120, default="Zadanie")

class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    lecturerID = models.ForeignKey(User, on_delete=models.PROTECT)




