from django.db import models

class Account(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class AccountDetails(models.Model):

class Stage(models.Model):
    name = models.CharField(max_length=50)

