# Generated by Django 2.1 on 2018-09-17 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_auto_20180917_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='stagestudent',
            name='complete',
            field=models.BooleanField(default=0),
        ),
    ]