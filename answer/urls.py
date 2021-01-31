from django.urls import re_path, path

from . import views

app_name = 'answer'

urlpatterns = [
	re_path(r'^briefing/results/(?P<brif_id>[-+]?\d+)/$', views.saving_answers, name='results'),
]