# Generated by Django 2.0.3 on 2018-11-13 15:14

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20181113_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='userabsence',
            name='absence_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='completed_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 13, 16, 14, 33, 95012)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 13, 16, 14, 33, 97012)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='end_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 20, 16, 14, 33, 95012)),
        ),
        migrations.AlterField(
            model_name='stagestudent',
            name='start_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 13, 16, 14, 33, 95012)),
        ),
    ]