# Generated by Django 2.1 on 2018-09-28 00:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('models', '0008_auto_20180928_0132'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAbsence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absence', models.BooleanField(default=0)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='closed',
            field=models.BooleanField(default=0),
        ),
    ]
