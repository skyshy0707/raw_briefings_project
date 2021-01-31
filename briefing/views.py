from django.shortcuts import render

# Create your views here.
from . import models
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Briefing
from .forms import Briefing_form
from question.models import Question
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from question.forms import AddQuestion

class DeleteBriefing(PermissionRequiredMixin, DeleteView):

	permission_required = ('question.delete_briefing')
	model = models.Briefing
	template_name_suffix = '_delete_form'
	success_url = reverse_lazy('briefing:briefings')
	
class UpdateBriefing(PermissionRequiredMixin, UpdateView):

	permission_required = ('question.edit_briefing')
	model = models.Briefing
	fields = ['name', 'description', 'date_end']
	template_name_suffix = '_edit_form'
	success_url = reverse_lazy('briefing:briefings')
	
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data["form_cr_q"] = AddQuestion()
		data["brif_id"] = self.get_object().id
		return data


@permission_required('briefing.add_briefing')
def add_briefing(request):

	if request.method == 'POST':
		br_form = Briefing_form(request.POST)
		if br_form.is_valid():
			br_form.save()
			return HttpResponseRedirect('/briefings/',)
		else:
			return render(request, 'add_brief.html', {'form': Briefing_form(), 
													  'errors': br_form.errors
													  }
													  )
			
	return render(request, 'add_brief.html', {'form': Briefing_form()})

def get_briefings(request,):
	briefs = Briefing.objects.all().order_by('id')
	return render(request, 'briefings.html', {"briefs": briefs})
	
def home(request):
	return render(request, 'home.html')
	
	