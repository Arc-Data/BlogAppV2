from django.urls import path 
from .views import *

urlpatterns = [
	path('', HomeView.as_view(), name = "home"),
	path('profile/<slug:slug>/', ProfileView.as_view(), name = "profile"),
]