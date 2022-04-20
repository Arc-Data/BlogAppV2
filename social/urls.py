from django.urls import path 
from .views import *

urlpatterns = [
	path('', HomeView.as_view(), name = "home"),
	path('submit/', CreatePost.as_view(), name = "create"),
	path('profile/<slug:slug>/', ProfileView.as_view(), name = "profile"),
]