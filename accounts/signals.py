from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.contrib.auth.models import User
from .models import Profile


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
		user.save()

		send_mail(
			"Your profile was updated!",
			"This message is being sent to you to let you know that your profile at sublimeimprovements.com has been successfully updated.",
			"noreply@sublimeimprovements.com",
			[profile.email],
			fail_silently=False,
		)

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
	try:
		user = instance.user
		user.delete()
	except:
		pass