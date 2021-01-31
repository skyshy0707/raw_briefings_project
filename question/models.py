from django.db import models
from django.contrib import admin

#from allauth.compat import python_2_unicode_compatible, ugettext_lazy as _
# Create your models here.

from briefing.models import Briefing

class Question(models.Model):
	briefing = models.ForeignKey(Briefing, on_delete = models.CASCADE)
	name = models.CharField(max_length = 255)
	date_create = models.DateField(editable=False, blank=True)
	
	


class Text_Ans(Question):
	ans = models.TextField()

class Variant_Ans(Question):
	
	is_oneVar = models.BooleanField()
	


class Variant_Ans_field(models.Model):
	question = models.ForeignKey(Variant_Ans, on_delete=models.CASCADE)
	ans = models.CharField(max_length = 255,)
	
admin.site.register(Question,)
admin.site.register(Variant_Ans,)
admin.site.register(Variant_Ans_field,)