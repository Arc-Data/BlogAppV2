from django.shortcuts import render
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):

		return render(request, 'social/home.html', {})


# Create your views here.
