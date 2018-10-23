# Generated by Django 2.1 on 2018-10-22 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20181010_0059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='stage',
            new_name='stageStudent',
        ),
        migrations.RemoveField(
            model_name='achievement',
            name='task',
        ),
        migrations.AlterField(
            model_name='answer',
            name='completed_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 22, 16, 42, 37, 295205)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 16, 42, 37, 295205)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 22, 16, 42, 37, 295205)),
        ),
        migrations.AlterField(
            model_name='userabsence',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 10, 22, 16, 42, 37, 295205)),
        ),
    ]