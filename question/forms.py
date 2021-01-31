from django import forms
from django.forms import modelformset_factory, formset_factory
from .models import Text_Ans, Variant_Ans_field, Variant_Ans



class AddQuestion(forms.Form):

	
	type_ans = forms.CharField(widget=forms.Select(choices=
									(('TXT', 'Текстовый'), 
									('VAR', 'Мультивариантный')
									)
									)
									)




class TextAns_form(forms.ModelForm):
	
	class Meta:
		model = Text_Ans
		fields = ['name',]
		labels = {'name':'Вопрос',}
		

from django.forms.fields import ChoiceField
from django.forms import inlineformset_factory
# Create your models here.


class Variant_Ans_form(forms.ModelForm):
	
	class Meta:
		model = Variant_Ans
		fields = ['name', 'is_oneVar',]
		labels = {'name':'Вопрос','is_oneVar': 'Вопрос с одним вариантом ответа'}

SelectVariants = inlineformset_factory(
	Variant_Ans, 
	Variant_Ans_field, 
	fields=('ans',),
	labels={'ans': 'Вариант',},
	extra=1, 
	widgets={'ans': forms.TextInput(
		attrs={'class': 'form-control',}
			)
			}
			)


class AnonymusUser(forms.Form):

	isAnonymus = forms.BooleanField(required=False)