from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import datetime
from django.urls import reverse, reverse_lazy
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

class DetailPostView(LoginRequiredMixin, View):
	def get(self, request, id, *args, **kwargs):
		post = Post.objects.get(id = id)
		context = {
			'post':post,
		}
		return render(request, 'social/post-detail.html', context)


class ProfileView(LoginRequiredMixin, View):
	def get(self, request, slug, *args, **kwargs):
		profile = Profile.objects.get(slug = slug)
		users = profile.followers.all()
		is_following = False

		for x in users:
			if self.request.user == x:
				is_following = True 
				break

		print(is_following)

		context = {
			'profile':profile,
			'is_following':is_following,
		}
		return render(request, 'social/profile.html', context)

class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	form_class = ProfileForm
	model = Profile
	template_name = 'social/profile-edit.html'


	def get_context_data(self, **kwargs):
		profile = self.get_object() 
		users = profile.followers.all();

		context = super().get_context_data(**kwargs)
		context['is_following'] = False 


		for x in users:
			if self.request.user == x:
				context['is_following'] = True

		print(context['is_following'])
		return context
	

	def test_func(self):
		return self.get_object() == self.request.user.profile 

	def get_success_url(self, **kwargs):
		return reverse_lazy('profile', kwargs = {'slug': self.kwargs['slug']})


class FollowProfile(LoginRequiredMixin, View):
	def post(self, request, slug, *args, **kwargs):
		profile = Profile.objects.get(slug = slug)
		profile.followers.add(request.user)

		return redirect('profile', slug)

class UnfollowProfile(LoginRequiredMixin, View):
	def post(self, request, slug, *args, **kwargs):
		profile = Profile.objects.get(slug = slug)
		profile.followers.remove(request.user)

		return redirect('profile', slug)
# Create your views here.
