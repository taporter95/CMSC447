from __future__ import unicode_literals
import datetime
import time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class Post(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.CharField(max_length=200, db_index=True)
	description = models.CharField(max_length=200)
	cost = models.FloatField(default=0)
	image = models.FileField(null=True, blank=True)
	post_type = models.CharField(max_length=20)
	creation_date = models.DateTimeField(db_index=True)