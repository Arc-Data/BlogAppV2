from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	username = models.CharField(max_length = 25, blank = True, null = True)
	profile_pic = models.ImageField(upload_to = 'uploads/profile_pictures', default = "uploads/profile_pictures/default-blue.png")
	banner_pic = models.ImageField(upload_to = 'uploads/banner_pictures', default = "uploads/banner_pictures/740377.png")

	def __str__(self):
		return self.username

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(
			user = instance,
			username = instance.username
			)
		print('Profile Attached')

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
