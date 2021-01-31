from django.urls import re_path, path

from . import views

app_name = 'briefing'

urlpatterns = [
	path('', views.home, name='home'),
	re_path(r'^briefings/$', views.get_briefings, name='briefings'),
	re_path(r'^briefings/briefing/add/$', views.add_briefing, name='add_brief'),
	re_path(r'^briefings/briefing/delete/(?P<pk>[-+]?\d+)/$', views.DeleteBriefing.as_view(), name='briefing_delete_form'),
	re_path(r'^briefings/briefing/edit/(?P<pk>[-+]?\d+)/$', views.UpdateBriefing.as_view(), name='briefing_edit_form'),
]