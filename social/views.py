from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.views.generic import View 
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile, Post
from .forms import PostForm

class HomeView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		form = PostForm
		posts = Post.objects.all()
		context = {
			'form':form,
			'posts':posts,
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

# Create your views here.
