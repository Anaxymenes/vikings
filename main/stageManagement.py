from django.contrib.auth.models import User
from models.models import *
from datetime import datetime, timedelta, timezone
from django.db import transaction
from django.db.models import Q