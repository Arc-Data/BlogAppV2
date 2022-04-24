from django.urls import path 
from .views import *

urlpatterns = [
	path('', HomeView.as_view(), name = "home"),
	path('submit/', CreatePostView.as_view(), name = "create"),
	
	path('post/<int:id>/', DetailPostView.as_view(), name = "post"),

	path('profile/<slug:slug>/', ProfileView.as_view(), name = "profile"),
	path('profile/<slug:slug>/follow', FollowProfile.as_view(), name = "follow-profile"),
	path('profile/<slug:slug>/unfollow', UnfollowProfile.as_view(), name = "unfollow-profile"),

	path('profile/<slug:slug>/edit', ProfileEdit.as_view(), name = "profile-edit"),

]