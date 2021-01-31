from . import models
from . import genForm as gf

def get_questionForms(brif_id):
	questions = models.Question.objects.filter(briefing__id=brif_id)
	q_forms=[]
	for question in questions:
		q_form = gf.questionClientForm(question)
		q_forms.append(q_form)
	return q_forms