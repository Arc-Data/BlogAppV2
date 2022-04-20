from django import forms
from django.forms import ModelForm 

from .models import Post, Profile 


class PostForm(forms.ModelForm):
	class Meta:
		model = Post 
		fields = ['body']