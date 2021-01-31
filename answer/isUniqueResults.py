from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from results.models import Results
from . import saveAnswers as san#6st error
from django.http import HttpResponseRedirect



def briefing_ids(ress):
	brief_ids = []
	for res in ress:
		brief_ids.append(res.briefing.id)
	return brief_ids

def have_passed_brief(brief_ids, brif_id):
	if int(brif_id) in brief_ids:
		return True
	return False

def isAnonymusUser(request):
	if not request.user.id:
		return True
	return False
	
def get_user_results(request):
	return Results.objects.filter(whorespond=request.user.id).union(
		   Results.objects.filter(user=request.user)
		   ).order_by("pk")

def isAnswered(request, brif_id):
	if isAnonymusUser(request):
		return True
	ress = get_user_results(request)	
	return have_passed_brief(briefing_ids(ress), brif_id)

		
