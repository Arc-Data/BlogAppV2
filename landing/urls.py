from django.urls import path 
from .views import *

urlpatterns = [
	path('', LandingView.as_view(), name = "landing-page"),
]