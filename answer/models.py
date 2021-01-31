from django.db import models
from django.contrib import admin
from results.models import Results
from question.models import Question
# Create your models here.

class Answer(models.Model):

	results = models.ForeignKey(Results, on_delete = models.CASCADE)
	question = models.ForeignKey(Question, on_delete = models.CASCADE)

class asTextArea(Answer):

	ans = models.TextField()

class asTextField(Answer):

	ans = models.CharField(max_length = 255,)

	

	
admin.site.register(Answer,)
admin.site.register(asTextArea,)
admin.site.register(asTextField,)

