from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile
import string, secrets, random

def generate_password(length):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
	if created:
		user = instance
		profile = Profile.objects.create(
			user = user,
			username = user.username,
			email = user.email,
			fname = user.first_name,
			lname = user.last_name,
		)
		profile.save()

		
@receiver(post_save, sender=Profile)
def updateProfile(sender, instance, created, **kwargs):
	profile = instance
	user = profile.user

	if created == False:
		user.first_name = profile.fname 
		user.last_name = profile.lname
		user.email = profile.email
		# user.is_staff = profile.is_staff
		# user.is_superuser = profile.is_superuser
		user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
	try:
		user = instance.user
		user.delete()
	except:
		pass