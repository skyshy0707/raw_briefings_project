from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from . import saveAnswers as sans
# Create your views here.

@login_required
def saving_answers(request, brif_id):
	
	if request.method == 'POST':
		sans.save_forms(request, brif_id)
		return HttpResponseRedirect('/briefings/')
		
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
def accessDenied_to_Briefing(request, brif_id):
	return render(request, 'access_denied_due_youve_answered.html')
