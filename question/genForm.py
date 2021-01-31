from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, HiddenInput
from .forms import SelectVariants, Variant_Ans_form, TextAns_form
from briefing.models import Briefing
from .models import Variant_Ans, Text_Ans, Question, Variant_Ans_field
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime


	
class ClientForm():
	
	def __init__(self,):
		self.suffix = '_clientForm'
		self.type_ = 'Text_Ans'
		self.choices = ()
		self.attrs = {
			'__module__': 'question.forms',
			'question_id': forms.CharField(
									initial='untitled', 
									max_length=255),
			}
		
	def set_type(self, a_type, mult):
		if mult:
			self.type_ = 'Variant_Ans_Many'
		else:
			self.type_ = a_type
		
	def set_choices(self, choices):
		self.choices = choices
		
	def set_obj_attrs(self, init):
		self.attrs.update({'name': forms.CharField(
									initial=init.name, 
									max_length=255),
							'question_id':forms.CharField(
									initial=init.id, 
									max_length=255,),
							'type_':forms.CharField(
									initial=self.type_, 
									max_length=255,)
									}
									)
	
	def get_metaclass(self,):
		return type(''.join((self.type_, self.suffix)),
											(forms.Form,),
											self.attrs
											) 
	def get_init_value(self, field):
		return str(field.initial)
		
	def get_class(self,):
		if self.type_ == 'Variant_Ans':
			return varsAns_f()
		elif self.type_ == 'Variant_Ans_Many':
			return varsAnsMany_f()
		return textAns_f()
		


class textAns_f(ClientForm):
	
	def __init__(self,):
		super().__init__()
		self.type_ = 'Text_Ans'
		
	def update(self,):
		self.attrs.update(
			{'ans': forms.CharField(widget=forms.Textarea), 
			'prefix': self.type_+self.get_init_value(
									self.attrs['question_id']
									),
			}
			)

class varsAns_f(ClientForm):
	
	def __init__(self,):
		super().__init__()
		self.type_ = 'Variant_Ans'
		
	
	def update(self,):
		self.attrs.update(
			{'ans': forms.ChoiceField(
								widget=RadioSelect, 
								choices=self.choices
								),
			'prefix': self.type_+self.get_init_value(
									self.attrs['question_id']
									),
			}
			)
			
class varsAnsMany_f(ClientForm):
	
	def __init__(self,):
		super().__init__()
		self.type_ = 'Variant_Ans_Many'
		
	def update(self,):
		self.attrs.update(
			{'ans': forms.MultipleChoiceField(
								widget=CheckboxSelectMultiple, 
								choices=self.choices
								),
			'prefix': self.type_+self.get_init_value(
									self.attrs['question_id']
									),
			}
			)

def get_choices(question):
	choices = Variant_Ans_field.objects.filter(
					question__id=question.id
					)	
	return [(choice.id, choice.ans) 
					for choice in choices
					]
	
def choices(type_, question):
	if type_ == "Text_Ans":
		return ()
	return get_choices(question)
	
	
def isMult(question):
	try:
		req_q = Variant_Ans.objects.get(pk=question.id)
		return not req_q.is_oneVar
	except ObjectDoesNotExist:
		return False


def typeQuestion(question, mult):
	try:
		Variant_Ans.objects.get(pk=question.id)
	except:
		return "Text_Ans"
	if mult:
		return "Variant_Ans_Many"
	return "Variant_Ans"
	
formsets = {"Text_Ans": textAns_f(), 
			"Variant_Ans": varsAns_f(), 
			"Variant_Ans_Many": varsAnsMany_f()
			}

def questionClientForm(question):
	mult = isMult(question)
	type_ = typeQuestion(question, mult)
	choices_ = choices(type_, question)
	form_class = ClientForm()
	form_class.set_type(type_, mult)
	form = form_class.get_class()
	form.set_choices(choices_)
	form.set_obj_attrs(question)
	form.update()
	return form.get_metaclass()



from .renderQuestions import renderAddQuestion#4st error

class GenForm():
	
	def __init__(self,):
		self.type_ = 'TXT'
		self.render = TextAns_form_gen()
		
	
	def set_type(self, atype):
		self.type_ = atype
		self.set_render()
	
	def set_render(self):
		if self.type_ == 'TXT':
			self.render =  TextAns_form_gen()
		else:
			self.render = Variant_Ans_form_gen()
		


			
class QForm():


	def __init__(self,):
		self.type_ = 'TXT'
		
	

class TextAns_form_gen(QForm):
	
	def __init__(self,):
		super().__init__()
		self.type_ = 'TXT'
		self.view = "question:save_textquestion"
		
	def get_render(self, request, brif_id):
		return renderAddQuestion(request, TextAns_form(), brif_id, self.view)
		

class Variant_Ans_form_gen(QForm):

	def __init__(self,):
		super().__init__()
		self.type_ = 'VAR'
		self.view = "question:save_varsquestion"
		
	def get_render(self, request, brif_id):
		return renderAddQuestion(request, Variant_Ans_form(), brif_id, self.view, SelectVariants())

def render(request, brif_id, type_):
	render = GenForm()
	render.set_type(type_)
	return render.render.get_render(request, brif_id)
	