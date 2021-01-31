from django.shortcuts import render
from .models import Results
from django.contrib.auth.decorators import login_required
from answer.models import asTextArea, asTextField
from answer.isUniqueResults import get_user_results
# Create your views here.



def get_set_Q(answers):
	return set([answer.question.name for answer in answers])
	
def get_blank_list_A(n):
	return [[] for i in range(n)]
	
def dictQA_init(answers):
	Q = get_set_Q(answers)
	A = get_blank_list_A(len(Q))
	return dict(zip(Q, A))


def get_set_QA(answers):
	QA = dictQA_init(answers)
	
	for answer in answers:
		QA[answer.question.name].append(answer.ans)
			
	return QA
	
def results_as_dict(res, QA):
	return {"res": res.briefing.name, "answers": QA}

@login_required
def view_results(request):

	ress = get_user_results(request)	   
	results_list = []
	for res in ress:
		answers = asTextArea.objects.filter(results=res).union(
					asTextField.objects.filter(results=res)
					).order_by("pk")
		results = results_as_dict(res, get_set_QA(answers))
		results_list.append(results)
	return render(request, 'user_results.html', {'results': results_list})
		