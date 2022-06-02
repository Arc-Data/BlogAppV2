from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.timezone import datetime
from django.urls import reverse, reverse_lazy
from django.views.generic import View 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Profile, Post, Comment
from .forms import PostForm, ProfileForm, CommentForm

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
		return reverse_lazy('home')

class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	form_class = PostForm 
	model = Post
	template_name = 'social/post-edit.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['previous'] = self.request.META.get('HTTP_REFERER')

		return context

	def test_func(self):
		return self.get_object().author == self.request.user.profile

	def get_success_url(self, **kwargs):
		return reverse_lazy('post', kwargs = {'pk':self.kwargs['pk']})


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	template_name = 'social/post-delete.html'
	model = Post 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['previous'] = self.request.META.get('HTTP_REFERER')

		return context

	def test_func(self):
		return self.get_object().author == self.request.user.profile 

	def get_success_url(self):
		return reverse('home')


class DetailPostView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		previous = self.request.META.get('HTTP_REFERER')
		current = self.request.build_absolute_uri()
		
		post = Post.objects.get(id = pk)
		form = CommentForm
		comments = Comment.objects.filter(post = post).order_by('-created_on')

		if previous == current + 'edit/' or previous == current + 'delete/':
			previous = None 

		context = {
			'post':post,
			'previous':previous,
			'form':form,
			'comments':comments,
		}
		return render(request, 'social/post-detail.html', context)

	def post(self, request, pk, *args, **kwargs):
		previous = self.request.META.get('HTTP_REFERER')
		current = self.request.build_absolute_uri()

		post = Post.objects.get(id = pk)
		form = CommentForm(request.POST)
		comments = Comment.objects.filter(post = post).order_by('-created_on')

		if previous == current + 'edit/' or previous == current + 'delete/':
			previous = None 

		if form.is_valid():
			new_comment = form.save(commit = False)
			new_comment.author = self.request.user.profile 
			new_comment.post = post 
			new_comment.save()

			return redirect('post', post.id)

		context = {
			'post':post,
			'previous':previous,
			'form':form,
			'comments':comments,
		}
		return render(request, 'social/post-detail.html', context)

class CommentReplyView(LoginRequiredMixin, View):
	def post(self, request, post_pk, pk, *args, **kwargs):
		post = Post.objects.get(id = post_pk)
		parent_comment = Comment.objects.get(id = pk)
		form = CommentForm(request.POST)

		if form.is_valid():
			new_comment = form.save(commit = False)
			new_comment.post = post
			new_comment.author = request.user.profile
			new_comment.parent = parent_comment
			new_comment.created_on = timezone.now()
			new_comment.save()

		return redirect('post', post_pk)

class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

	template_name = 'social/delete-comment.html'
	model = Comment

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['previous'] = self.request.META.get('HTTP_REFERER')

		return context

	def test_func(self):
		return self.get_object().author == self.request.user.profile 

	def get_success_url(self, **kwargs):
		print(kwargs)
		print("Hello")
		return reverse_lazy('post', kwargs = {'pk': self.kwargs['post_pk']})

class EditCommentView(View):
	pass


class ProfileView(LoginRequiredMixin, View):
	def get(self, request, slug, *args, **kwargs):
		profile = Profile.objects.get(slug = slug)
		posts = Post.objects.filter(author = profile).order_by('-created_on')
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
			'posts':posts,
		}
		return render(request, 'social/profile-overview.html', context)

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
