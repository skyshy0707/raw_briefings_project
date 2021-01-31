from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
# Create your models here.

class UsualUser(AbstractUser):
	
	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		is_superuser = request.user.is_superuser
		disabled_fields = set()  # type: Set[str]
		if not is_superuser:
			disabled_fields |= {
                'username',
                'is_superuser',
            }
		for f in disabled_fields:
			if f in form.base_fields:
				form.base_fields[f].disabled = True
		return form
	

admin.site.register(UsualUser)