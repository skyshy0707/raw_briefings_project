from django.urls import re_path, path

from . import views
from answer import views as ans_views

app_name = 'question'


urlpatterns = [
	re_path(r'^briefing/add_question/(?P<brif_id>[-+]?\d+)/$', views.create_question, name='add_question'),
	re_path(r'^briefing/save_question_as_text/(?P<brif_id>[-+]?\d+)/$', views.save_textquestion, name='save_textquestion'),
	re_path(r'^briefing/save_question_as_multvars/(?P<brif_id>[-+]?\d+)/$', views.save_varsquestion, name='save_varsquestion'),
	re_path(r'^briefing/questions/(?P<brif_id>[-+]?\d+)/denied/$', ans_views.accessDenied_to_Briefing, name='access_denied_to_briefing'),
	re_path(r'^briefing/questions/(?P<brif_id>[-+]?\d+)/edit=(?P<edit>\d{1})/$', views.view_briefings_questions, name='questions'),
	re_path(r'^briefing/(?P<brif_id>[-+]?\d+)/svquestion/delete/(?P<pk>[-+]?\d+)/$', views.DeleteTextQuestion.as_view(), name='svquestion_delete_form'),
	re_path(r'^briefing/(?P<brif_id>[-+]?\d+)/svquestion/edit/(?P<pk>[-+]?\d+)/$', views.UpdateTextQuestion.as_view(), name='svquestion_edit_form'),
	re_path(r'^briefing/(?P<brif_id>[-+]?\d+)/mvquestion/delete/(?P<pk>[-+]?\d+)/$', views.DeleteMultivarQuestion.as_view(), name='mvquestion_delete_form'),
	re_path(r'^briefing/(?P<brif_id>[-+]?\d+)/mvquestion/edit/(?P<pk>[-+]?\d+)/$', views.UpdateMultivarQuestion.as_view(), name='mvquestion_edit_form'),
]