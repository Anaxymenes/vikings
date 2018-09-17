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

class StageTasks(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)
    description = models.CharField(max_length=2500)
    title = models.CharField(max_length=120, default="Zadanie")
    points = models.IntegerField(default=5)
    exp_points = models.IntegerField(default=20)
    sampleAnswer = models.CharField(max_length=2500)


class AchievementTask(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete = models.PROTECT)
    task = models.ForeignKey(StageTasks, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

class Answer(models.Model):
    student = models.ForeignKey(User, on_delete = models.CASCADE)
    task = models.ForeignKey(StageTasks, on_delete=models.PROTECT)
    answerSql = models.CharField(max_length=2500)

class StageStudent(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    databaseSql = models.CharField(max_length=5000)
    complete = models.BooleanField(default=0)

class StudentGroup(models.Model):
    name = models.CharField(max_length=50)
    lecturer = models.ForeignKey(User, on_delete=models.PROTECT)




