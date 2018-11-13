from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

def getGroupByIdShortDetails(group_id):
    return Group.objects.filter(id=group_id).first()