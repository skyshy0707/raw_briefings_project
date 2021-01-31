from django.shortcuts import render, redirect
from answer import isUniqueResults as isUnres#5st error


def isAnswered(request, brif_id):
	return isUnres.isAnswered(request, brif_id)

	
def redirect_denied(brif_id):	
	return redirect(brif_id.join(('/briefing/questions/', '/denied',)))

def renderQuestions(request, template, q_forms, brif_id, anonymus_form=None):
	return render(request, template, {"q_forms": q_forms, 
									  "brif_id": brif_id, 
									  "anonymus": anonymus_form,
									  }
									  )
def renderAddQuestion(request, q_form, brif_id, view, fields=None):
	return render(request, 'add_question.html', {"q_form": q_form, 
												"fields": fields, 
												"brif_id": brif_id,
												"view": view,
												}
												)
									  
def access_to_edit(request, q_forms, brif_id):
	if request.user.is_staff:
		return renderQuestions(request, 'edit_questions.html', q_forms, brif_id)
	return redirect_denied(brif_id)
									  
									