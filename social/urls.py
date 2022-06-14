from django.urls import path 
from .views import *

urlpatterns = [
	path('', HomeView.as_view(), name = "home"),
	path('submit/', CreatePostView.as_view(), name = "create"),
	
	path('post/<int:pk>/', DetailPostView.as_view(), name = "post"),

	path('post/<int:pk>/like', AddLikeView.as_view(), name = "like"),
	path('post/<int:pk>/edit/', EditPostView.as_view(), name = 'post-edit'),
	path('post/<int:pk>/delete/', DeletePostView.as_view(), name = "post-delete"),
	path('post/<int:post_pk>/thread/<int:comment_pk>/', CommentThreadView.as_view(), name = "comment-thread"),

	path('post/<int:post_pk>/<int:pk>/reply', CommentReplyView.as_view(), name = "add-reply"),
	path('post/<int:post_pk>/<int:pk>/delete', DeleteCommentView.as_view(), name = "delete-comment"),
	path('post/<int:post_pk>/<int:pk>/update', EditCommentView.as_view(), name = "edit-comment"),
	path('post/<int:post_pk>/<int:pk>/like', AddCommentLikeView.as_view(), name = "add-comment-like"),


	path('profile/<slug:slug>/', ProfileView.as_view(), name = "profile"),
	path('profile/<slug:slug>/follow/', FollowProfile.as_view(), name = "follow-profile"),
	path('profile/<slug:slug>/unfollow/', UnfollowProfile.as_view(), name = "unfollow-profile"),

	path('notification/<int:notif_pk>/', NotificationRedirectView.as_view(), name = "notif-redirect"),

	path('profile/<slug:slug>/edit', ProfileEdit.as_view(), name = "profile-edit"),

]