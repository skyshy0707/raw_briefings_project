from django.shortcuts import render

# Create your views here.

from .forms import TextAns_form, SelectVariants, Variant_Ans_field, AddQuestion, Variant_Ans_form, AnonymusUser
from . import genForm as gf

from django.views.generic.edit import UpdateView, DeleteView
from . import models
from briefing.models import Briefing
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from . import saveQuestions as saveQ
from . import renderQuestions as rendQ
from . import getQuestions as getQ

class DeleteMultivarQuestion(PermissionRequiredMixin, DeleteView):
	
	permission_required = ('question.delete_variant_ans')
	model = models.Variant_Ans
	template_name_suffix = '_delete_form'
	
	def get_success_url(self,):
		return reverse_lazy('question:questions', 
							kwargs={'brif_id': self.kwargs['brif_id'] , 'edit': '1'}, 
							)
							
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return self.render_to_response(self.get_context_data(
				brif_id=self.kwargs["brif_id"]
				)
				)

class DeleteTextQuestion(PermissionRequiredMixin, DeleteView):

	permission_required = ('question.delete_text_ans')
	model = models.Text_Ans
	template_name_suffix = '_delete_form'
	
	def get_success_url(self,):
		return reverse_lazy('question:questions', 
							kwargs={'brif_id': self.kwargs['brif_id'] , 'edit': '1'}, 
							)
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return self.render_to_response(self.get_context_data(
				brif_id=self.kwargs["brif_id"]
				)
				)
				
class UpdateMultivarQuestion(PermissionRequiredMixin, UpdateView):
	
	permission_required = ('question.edit_variant_ans')
	model = models.Variant_Ans
	template_name_suffix = '_update_form'
	form_class = Variant_Ans_form
	
	def get_success_url(self,):
		return reverse_lazy('question:questions', 
							kwargs={'brif_id': self.kwargs['brif_id'] , 'edit': '1'}, 
							)
	
	def get_variants(self,):
		question = self.get_object()
		return Variant_Ans_field.objects.all().filter(question__id=question.id)
	
	def get_variants_asform(self,):
		formset = SelectVariants(instance=self.get_object())
		formset.extra=0
		return formset
		
	def get_question_asform(self,):
		return self.get_form(self.get_form_class())
	
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		q_form = self.get_question_asform()
		return self.render_to_response(self.get_context_data(
				form=q_form, var_forms=self.get_variants_asform(),
				brif_id=self.kwargs["brif_id"]
				)
				)
	
	def post(self, request, *args, **kwargs):	
		self.object = self.get_object()
		form = self.get_question_asform()
		var_forms = SelectVariants(self.request.POST, instance=self.object)
		if var_forms.is_valid() and form.is_valid():
			return self.form_valid(form, var_forms)
		return self.form_invalid(form, var_forms)
		
	def form_valid(self, q_form, form):	
		self.object = q_form.save()
		form.instance = self.object
		form.save()
		return HttpResponseRedirect(self.get_success_url())
	
	def form_invalid(self, q_form, form):
		return self.render_to_response(self.get_context_data(q_form=q_form, 
															form=form
															)
															)
		
class UpdateTextQuestion(PermissionRequiredMixin, UpdateView):

	permission_required = ('question.edit_text_ans')
	model = models.Text_Ans
	template_name_suffix = '_update_form'
	form_class = TextAns_form

	
	def get_success_url(self,):
		return reverse_lazy('question:questions', 
							kwargs={'brif_id': self.kwargs['brif_id'] , 
									'edit': '1'
									}
									)
									
	
	def get_question_asform(self,):
		return self.get_form(self.get_form_class())
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		q_form = self.get_question_asform()
		return self.render_to_response(self.get_context_data(
				form=q_form,
				brif_id=self.kwargs["brif_id"]
				)
				)

	
@permission_required('question.add_question')	
def create_question(request, brif_id):
	br = Briefing.objects.get(pk=brif_id)
	if request.method == 'POST':
		form = AddQuestion(request.POST)
		if form.is_valid():
			return gf.render(request, brif_id, form.cleaned_data['type_ans'])

	return redirect('/briefing/add_question/' + str(brif_id) + '/')
	
@permission_required('question.add_question')	
def save_textquestion(request, brif_id):
	br = Briefing.objects.get(pk=brif_id)
	q_form = TextAns_form(request.POST)
	if q_form.is_valid():
		saveQ.save_question(brif_id, q_form)
		return HttpResponseRedirect('/briefings/briefing/edit/' + str(brif_id))
		
	return rendQ.renderAddQuestion(request, q_form, brif_id, 
									"question:save_textquestion")
	
			 
@permission_required('question.add_question')	
def save_varsquestion(request, brif_id):
	if request.method == 'GET':
		q_form = Variant_Ans_form(request.GET or None)
		fields = SelectVariants(queryset=Variant_Ans_field.objects.none())
	elif request.method == "POST":
		q_form = Variant_Ans_form(request.POST)
		if q_form.is_valid():
			return saveQ.save_filled_fields(request, brif_id, q_form)
			
	return rendQ.renderAddQuestion(request, q_form, brif_id, 
									"question:save_varsquestion", fields 
									)
	
		

def view_briefings_questions(request, brif_id, edit):

	q_forms = getQ.get_questionForms(brif_id)

	if bool(int(edit)):
		return rendQ.access_to_edit(request, q_forms, brif_id)

	if rendQ.isAnswered(request, brif_id):
		return rendQ.redirect_denied(brif_id)
	
	return rendQ.renderQuestions(request, 'questions.html', q_forms, brif_id, AnonymusUser())
	
