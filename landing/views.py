from django.shortcuts import render
from django.views.generic import View 


class LandingView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'landing/landing.html', {})

# Create your views here.
