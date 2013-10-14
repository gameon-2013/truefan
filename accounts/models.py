from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	"""docstring for ClassName"""
	user = models.ForeignKey(User)
	#profilePic = models.ImageField(blank = True, null = True)

	def __str__(self):
		return self.name
	class Admin:
		pass

