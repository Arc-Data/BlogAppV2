from django import forms
from django.forms import ModelForm 

from .models import Post, Profile 


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