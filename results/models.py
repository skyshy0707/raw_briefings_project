from django.db import models
from briefing.models import Briefing
from user.models import UsualUser
from django.contrib import admin
# Create your models here.

class Results(models.Model):
	
	briefing = models.ForeignKey(Briefing, on_delete=models.CASCADE)
	user = models.ForeignKey(UsualUser, blank=True, null=True, on_delete=models.SET_NULL)
	whorespond = models.IntegerField(null=True, blank=True)

admin.site.register(Results)