from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta, date
from django.utils import timezone

class AccountDetails(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    hp_max = models.IntegerField(default=100)
    current_hp = models.IntegerField(default=100)
    level = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    exp_max = models.IntegerField(default=100)
    current_exp = models.IntegerField(default=0)
    
class Stage(models.Model):
    name = models.CharField(max_length=50)

class DifficultyLevel(models.Model):
    level = models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)])
    title = models.CharField(max_length=120)

class StageTasks(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)
    description = models.CharField(max_length=2500)
    points = models.IntegerField(default=5)
    exp_points = models.IntegerField(default=20)
    sampleAnswer = models.CharField(max_length=2500)
    prompt = models.CharField(max_length = 2500)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete = models.CASCADE)

class UserAbsence(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    absence = models.BooleanField(default=0)
    date = models.DateField(default=datetime.now())

class Achievement(models.Model):
    name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    picture = models.CharField(max_length=250,default="404.png")

class AchievementTask(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete = models.PROTECT)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

class StageStudent(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    databaseSql = models.CharField(max_length=5000)
    complete = models.BooleanField(default=0)
    start_at = models.DateTimeField(default=datetime.now())
    end_at = models.DateTimeField(default=datetime.now()+timedelta(days=7))

class Answer(models.Model):
    stageStudent = models.ForeignKey(StageStudent, on_delete = models.CASCADE)
    task = models.ForeignKey(StageTasks, on_delete=models.PROTECT)
    answerSql = models.CharField(max_length=2500)
    usedPrompt = models.BooleanField(default=0)
    note = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)], default=0)
    rated = models.BooleanField(default=0)
    completed = models.BooleanField(default=0)
    completed_at = models.DateTimeField(default=datetime.now())

class Group(models.Model):
    name = models.CharField(max_length=50)
    lecturer = models.ForeignKey(User, on_delete=models.PROTECT)

class StudentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    student = models.ForeignKey(User, on_delete = models.CASCADE)

class StoryLevel(models.Model):
    stage = models.ForeignKey(Stage, on_delete = models.CASCADE)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete = models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.CharField(max_length=1200)

class Messages(models.Model):
    from_user = models.ForeignKey(User, related_name='messageFrom', on_delete = models.CASCADE, blank = True, null=True)
    to_user = models.ForeignKey(User,related_name='to_user_Message', on_delete = models.CASCADE)
    title = models.CharField(max_length=120)
    message = models.CharField(max_length=2000)
    is_read = models.BooleanField(default=0)
    send_date = models.DateTimeField(default=datetime.now())
    delete_for_from_user = models.BooleanField(default=0)
    delete_for_to_user = models.BooleanField(default=0)

class MessagesAnswer(models.Model):
    message = models.ForeignKey(Messages, related_name="messageId", on_delete=models.CASCADE)
    answer_tois_created = models.ForeignKey(Messages,related_name='answerMessage', on_delete=models.CASCADE)    
