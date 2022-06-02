from django import forms
from django.forms import ModelForm 

from .models import Post, Profile, Comment


class PostForm(forms.ModelForm):
	body = forms.CharField(widget = forms.Textarea(
		attrs = {
			"class":"text-input",
			"placeholder":"What's on your mind?",
		}))

	class Meta:
		model = Post 
		fields = ['body']


class ProfileForm(forms.ModelForm):

	class Meta:
		model = Profile 
		fields = ['username', 'profile_pic', 'banner_pic']

class CommentForm(forms.ModelForm):
	content = forms.CharField(widget = forms.TextInput(
		attrs = {
			'class':'comment-input',
			'placeholder':'Write a comment!'
		}
		))

	class Meta:
		model = Comment 
		fields = ['content']