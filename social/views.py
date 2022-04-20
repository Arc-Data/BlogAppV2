from django.shortcuts import render
from django.views.generic import View 
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile
from .forms import PostForm

class HomeView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		form = PostForm
		context = {
			'form':form,
		}
		return render(request, 'social/home.html', context)


class ProfileView(LoginRequiredMixin, View):
	def get(self, request, slug, *args, **kwargs):
		profile = Profile.objects.get(slug = slug)

		context = {
			'profile':profile,
		}
		return render(request, 'social/profile.html', context)

# Create your views here.
