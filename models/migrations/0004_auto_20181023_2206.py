# Generated by Django 2.1 on 2018-10-23 20:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_auto_20181022_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='completed_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 23, 22, 6, 30, 897810)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 30, 22, 6, 30, 896306)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 23, 22, 6, 30, 896306)),
        ),
        migrations.AlterField(
            model_name='userabsence',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 10, 23, 22, 6, 30, 894302)),
        ),
    ]