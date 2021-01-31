from django.http import HttpResponseRedirect

from briefing.models import Briefing
from datetime import datetime
from .forms import SelectVariants
from .renderQuestions import renderAddQuestion

def save_question(brif_id, form):
	br = Briefing.objects.get(pk=brif_id)
	question = form.save(commit=False)
	question.briefing = br
	question.date_create = datetime.now()
	question.save()
	return question
	

def saveInlineFormset(decorated_method):
	def save(request, brif_id, base_form):
		question = save_question(brif_id, base_form)
		fields = SelectVariants(request.POST, instance=question)
		return decorated_method(request, brif_id, base_form, fields)
	return save


@saveInlineFormset		
def save_filled_fields(request, brif_id, base_form, filled_fields):
	if filled_fields.is_valid():
		filled_fields.save()
		return HttpResponseRedirect('/briefings/briefing/edit/' + str(brif_id))
	return renderAddQuestion(request, base_form, brif_id, 
							"question:save_varsquestion",
							 filled_fields
							 )