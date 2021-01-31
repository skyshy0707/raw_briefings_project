from django.db import models
from user.models import UsualUser
# Create your models here.
from django.contrib import admin

class Briefing(models.Model):
	
	name = models.CharField(max_length=35, editable=True)
	description = models.TextField(editable=True)
	date_begin = models.DateField(editable=True)
	date_end = models.DateField(editable=True)


admin.site.register(Briefing)