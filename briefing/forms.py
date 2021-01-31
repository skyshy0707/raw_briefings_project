from django import forms
from .models import Briefing

class Briefing_form(forms.ModelForm):
	
	class Meta:
		model = Briefing
		
		fields = ['name', 'description', 'date_begin', 'date_end']
		labels = {
				  'name': 'Название опроса  ', 
				  'description': 'Описание ', 
				  'date_begin': 'Дата начала опроса', 
				  'date_end': 'Дата завершения опроса'
				  }

	