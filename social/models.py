from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.utils.text import slugify


from PIL import Image

class Post(models.Model):
	author = models.ForeignKey('Profile', blank = True, null = True,on_delete = models.CASCADE)
	body = models.TextField()
	created_on = models.DateTimeField(editable = False)
	likes = models.ManyToManyField(User, blank = True, related_name = "likes")

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_on = timezone.now()
		
		return super(Post, self).save(*args, **kwargs)

	@property 
	def comments(self):
		return len(Comment.objects.filter(post = self))


class Comment(models.Model):
	post = models.ForeignKey('Post', on_delete = models.CASCADE, blank = True)
	author = models.ForeignKey('Profile', on_delete = models.CASCADE, blank = True)	
	content = models.CharField(max_length = 200, blank = True)
	created_on = models.DateTimeField(editable = False)
	parent = models.ForeignKey('self', on_delete = models.CASCADE, blank = True, null = True)
	likes = models.ManyToManyField(User, blank = True, related_name = "comment_likes")

	def save(self, *args, **kwargs):
		if not self.id:
			self.created_on = timezone.now() 

		return super(Comment, self).save(*args, **kwargs)

	@property
	def children(self):
		return Comment.objects.filter(parent = self).order_by('created_on').all()

	@property 
	def is_parent(self):
		if self.parent is None:
			return True
		return False
	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	username = models.CharField(max_length = 25, blank = True, null = True, unique =True)
	profile_pic = models.ImageField(upload_to = 'uploads/profile_pictures', default = "uploads/profile_pictures/default-blue.png")
	banner_pic = models.ImageField(upload_to = 'uploads/banner_pictures', default = "uploads/banner_pictures/740377.png")
	date_joined = models.DateField(editable = False)
	slug = models.SlugField(unique = True)
	followers = models.ManyToManyField(User, blank = True, related_name = 'followers')

	def __str__(self):
		return self.username



@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(
			user = instance,
			username = instance.username,
			slug = slugify(instance.username),
			date_joined = timezone.now()
			)
		print('Profile Attached')

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


class Notification(models.Model):
	notif_type = models.IntegerField(blank = True)
	to_user = models.ForeignKey(User, related_name = "notification_to", null = True, on_delete = models.CASCADE)
	from_user = models.ForeignKey(User, related_name = "notification_from", null = True, on_delete = models.CASCADE)
	post = models.ForeignKey('Post', related_name = "+", blank = True, null = True, on_delete = models.CASCADE)
	comment = models.ForeignKey('Comment', related_name = "+", blank = True, null = True, on_delete = models.CASCADE)
	date = models.DateTimeField(default = timezone.now)
	user_has_seen = models.BooleanField(default = False)