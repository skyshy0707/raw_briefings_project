from django.urls import re_path, path

from . import views

app_name = 'user'

urlpatterns = [
	re_path(r'^signup/', views.create_user, name='signup'),
]