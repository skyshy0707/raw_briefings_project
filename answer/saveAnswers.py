from .models import asTextArea, asTextField
from question.models import Question, Variant_Ans_field
from results.models import Results
from briefing.models import Briefing
from user.models import UsualUser
from question.forms import AnonymusUser
from question.genForm import formsets
from django.core.exceptions import ValidationError

import copy

class FormAttrs():

	def __init__(self, brif_id):
		self.brif_id = brif_id
		self.question_ids = self.get_question_ids()

	def get_question_ids(self):
		questions = Question.objects.filter(briefing__id=self.brif_id)
		return [str(question.id) for question in questions]
	

	def get_varisnts(self, question_id):
		return Variant_Ans_field.objects.filter(question__id=int(question_id))
	
	def get_choices(self, formset, question_id):
		if formset in ("Variant_Ans", "Variant_Ans_Many"):
			vars = self.get_varisnts(question_id)
			return [(var.id, var.ans) for var in vars]
		return []
		
	def update_formclass(self, formclass, prefix):
		print("formclass_attrs", formclass.attrs, "formclass",  formclass)
		formclass.update()
		formclass = formclass.get_metaclass()
		formclass.prefix = prefix
		return formclass

	def get_formClass(self, formset, question_id):
		prefix = ''.join((formset, question_id))
		formclass = copy.deepcopy(formsets[formset])
		choices = self.get_choices(formset, question_id)
		formclass.set_choices(choices)
		return self.update_formclass(formclass, prefix)


	def get_formName(self, request, question_id):
		for str_ in request.POST.keys():
			for formset in formsets.keys():
				if str_.startswith(''.join((formset, question_id))):
					formclass = self.get_formClass(formset, question_id)
					return formclass, ''.join((formset, question_id)), formset
		return None
		

	def get_formPrefix(self, request,):
		for q_id in self.question_ids:
			yield self.get_formName(request, q_id)
			



class ValidatingFSets():
	def __init__(self,):
		self.forms = []
		self.valid_fsets = []
		self.Errors=[]
		self.type_ = None
		self.saveMethod = SaveTextAns()
	
	def is_valid(self, filled_form, form):
		try:
			filled_form.is_valid()
		except:
			print("ошибка инициализации", filled_form)
			ValidationError("Данная форма", form, "не прошла проверку")
		else:
			self.valid_fsets.append((filled_form, form))
	
	
	def set_forms(self, form_attrs, request):
		for class_, prefix, form in list(form_attrs):
			filled = class_(request.POST, prefix=prefix)
			self.is_valid(filled, form)
	
	
	def saving_forms(self, res):
		for form, name in self.valid_fsets:
			self.set_typeAns(name)
			self.saveMethod.saveAns(form, res)
			
	def set_typeAns(self, type_):
		self.saveMethod = Save().get_type(type_)
		
class Save():

		
	def saveAns(self):
		pass
	
	def get_type(self, type_):
		if type_ == 'Text_Ans':
			return SaveTextAns()
		elif type_ == 'Variant_Ans':
			return SaveVariantAns()
		return SaveVariantAnsMany()


class SaveTextAns(Save):
	
	def saveAns(self, form, res):
		question = Question.objects.get(pk=form.cleaned_data['question_id'])
		answer = asTextArea(ans=form.cleaned_data['ans'],
							results=res,
							question=question
							)
		answer.save()
	

class SaveVariants(Save):
	
	def get_ans_asText(self, id):
		ans = Variant_Ans_field.objects.get(pk=id)
		return ans.ans

class SaveVariantAns(SaveVariants):
	
	def saveAns(self, form, res):
		question = Question.objects.get(pk=form.cleaned_data['question_id'])
		answer = asTextField(ans=self.get_ans_asText(form.cleaned_data['ans']),
							 results=res,
							 question=question
							 )
		answer.save()
		
class SaveVariantAnsMany(SaveVariants):
	
	def saveAns(self, form, res):
		question = Question.objects.get(pk=form.cleaned_data['question_id'])
		for field in form.cleaned_data['ans']:
			answer = asTextField(ans=self.get_ans_asText(field),
								 results=res,
								 question=question
								 )
			answer.save()			
	

def form_attrs(request, brif_id):
	fattrs = FormAttrs(brif_id)
	return fattrs.get_formPrefix(request)
	
	
def newResults(request, brif_id):
	isAnonymus = AnonymusUser(request.POST)
	if isAnonymus.is_valid():
		if isAnonymus.cleaned_data['isAnonymus']:
			return Results(
							briefing=Briefing.objects.get(pk=brif_id),
							whorespond=request.user.id
							)
		return Results(
						briefing=Briefing.objects.get(pk=brif_id),
						user=UsualUser.objects.get(pk=request.user.id)
						)
	
def saving_forms(f_attrs, request, brif_id):
	vs = ValidatingFSets()
	vs.set_forms(f_attrs, request)
	res = newResults(request, brif_id)
	res.save()
	vs.saving_forms(res)

def save_forms(request, brif_id):
	f_attrs = form_attrs(request, brif_id)
	saving_forms(f_attrs, request, brif_id)
	
	