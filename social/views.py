from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import datetime
from django.urls import reverse
from django.views.generic import View 
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Profile, Post
from .forms import PostForm, ProfileForm

class HomeView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		form = PostForm
		posts = Post.objects.all().order_by('-created_on')
		current_time = timezone.now()
		context = {
			'form':form,
			'posts':posts,
			'current_time': current_time,
		}
		return render(request, 'social/home.html', context)


class CreatePostView(CreateView):
	form_class = PostForm
	template_name = 'social/create-post.html'

	def form_valid(self, form):
		form.instance.author = self.request.user.profile 

		return super().form_valid(form)

	def get_success_url(self):
		return reverse('home')

class ProfileView(LoginRequiredMixin, View):
	def get(self, request, slug, *args, **kwargs):
		profile = Profile.objects.get(slug = slug)
		context = {
			'profile':profile,
		}
		return render(request, 'social/profile.html', context)

class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	form_class = ProfileForm
	model = Profile
	template_name = 'social/profile-edit.html'

	def test_func(self):
		print(self.get_object())
		return self.get_object() == self.request.user.profile 


# Create your views here.
