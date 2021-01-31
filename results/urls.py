from django.urls import re_path, path

from . import views

app_name = 'results'

urlpatterns = [
	re_path(r'^briefing/results/yourresults/$', views.view_results, name='users_results'),
]