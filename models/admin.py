from django.contrib import admin
from .models import AccountDetails, Achievement, Stage, Task, AchievementTask, Answer, StageStudent, StageTasks, StudentGroup

admin.site.register(AccountDetails)
admin.site.register(Achievement)
admin.site.register(Stage)
admin.site.register(Task)
admin.site.register(AchievementTask)
admin.site.register(Answer)
admin.site.register(StageStudent)
admin.site.register(StageTasks)
admin.site.register(StudentGroup)

# Register your models here.
