from django.shortcuts import render
from .forms import UserCreation_form
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse

from . import assign_perm as apr

def create_user(request):
	if request.method == "POST":
		u_form = UserCreation_form(request.POST)
		if u_form.is_valid():
			u_form.save()
			apr.specify_perm()
			return HttpResponseRedirect('/')
			
	return render(request, 'signup.html', {"form": UserCreation_form()})
		
