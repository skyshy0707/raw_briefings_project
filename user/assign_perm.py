from .models import UsualUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from briefing.models import Briefing
from results.models import Results
from question.models import Question, Variant_Ans_field


def get_perm(a_model):
	content_type = ContentType.objects.get_for_model(a_model)
	return Permission.objects.filter(content_type=content_type)
	

def get_list_perm(listModels):
	permutations = []
	for model in listModels:
		permutations.extend(get_perm(model))
	return permutations
	

def get_accessed_perms():
	accessed_perms = ("view_briefing", 
					  "view_results", 
					  "add_results", 
					  "view_question",
					  "view_variant_ans_field",
					  )
	u_user_permissions = get_list_perm([
										Briefing, 
										Results, 
										Question, 
										Variant_Ans_field,
										]
										)
	return [p for p in u_user_permissions if p.codename in accessed_perms]
	


def specify_perm():

	add_perms = get_accessed_perms()											
	u = UsualUser.objects.last()
	user_id = u.id
	for perm in add_perms:
		u.user_permissions.add(perm)

	u.save()