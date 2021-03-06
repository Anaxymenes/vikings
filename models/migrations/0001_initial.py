# Generated by Django 2.1 on 2018-11-13 00:43

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hp_max', models.IntegerField(default=100)),
                ('current_hp', models.IntegerField(default=100)),
                ('level', models.IntegerField(default=1)),
                ('points', models.IntegerField(default=0)),
                ('exp_max', models.IntegerField(default=100)),
                ('current_exp', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('points', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=200)),
                ('picture', models.CharField(default='404.png', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='AchievementTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.Achievement')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerSql', models.CharField(max_length=2500)),
                ('usedPrompt', models.BooleanField(default=0)),
                ('note', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('rated', models.BooleanField(default=0)),
                ('completed', models.BooleanField(default=0)),
                ('completed_at', models.DateTimeField(default=datetime.datetime(2018, 11, 13, 1, 43, 12, 74180))),
            ],
        ),
        migrations.CreateModel(
            name='DifficultyLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('title', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('message', models.CharField(max_length=2000)),
                ('is_read', models.BooleanField(default=0)),
                ('send_date', models.DateTimeField(default=datetime.datetime(2018, 11, 13, 1, 43, 12, 74180))),
                ('delete_for_from_user', models.BooleanField(default=0)),
                ('delete_for_to_user', models.BooleanField(default=0)),
                ('from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messageFrom', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user_Message', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MessagesAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answerMessage', to='models.Messages')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messageId', to='models.Messages')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StageStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('databaseSql', models.CharField(max_length=5000)),
                ('complete', models.BooleanField(default=0)),
                ('start_at', models.DateTimeField(default=datetime.datetime(2018, 11, 13, 1, 43, 12, 74180))),
                ('end_at', models.DateTimeField(default=datetime.datetime(2018, 11, 20, 1, 43, 12, 74180))),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.Stage')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StageTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2500)),
                ('points', models.IntegerField(default=5)),
                ('exp_points', models.IntegerField(default=20)),
                ('sampleAnswer', models.CharField(max_length=2500)),
                ('prompt', models.CharField(max_length=2500)),
                ('difficulty_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.DifficultyLevel')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.Stage')),
            ],
        ),
        migrations.CreateModel(
            name='StoryLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('content', models.CharField(max_length=1200)),
                ('difficulty_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.DifficultyLevel')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Stage')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.Group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAbsence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absence', models.BooleanField(default=0)),
                ('date', models.DateField(default=datetime.datetime(2018, 11, 13, 1, 43, 12, 74180))),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='stageStudent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='models.StageStudent'),
        ),
        migrations.AddField(
            model_name='answer',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='models.StageTasks'),
        ),
    ]
