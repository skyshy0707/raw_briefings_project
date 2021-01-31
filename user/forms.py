from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsualUser
from django import forms

class UserCreation_form(UserCreationForm):

	class Meta:
		model = UsualUser
		fields = ("username", "email", "password1", "password2")