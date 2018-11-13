# Generated by Django 2.0.3 on 2018-11-13 15:03

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userabsence',
            name='date',
        ),
        migrations.AddField(
            model_name='userabsence',
            name='lesson_nr',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='answer',
            name='completed_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 13, 16, 3, 15, 353812)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 13, 16, 3, 15, 355812)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 20, 16, 3, 15, 352812)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 13, 16, 3, 15, 352812)),
        ),
    ]
