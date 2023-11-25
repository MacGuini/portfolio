from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from django.contrib.auth.models import User
from .models import Profile
import string, secrets, random

def generate_password(length):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


		
@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
	profile = instance
	# user = profile.user
	if created:
		profile = instance 

		fname = str(profile.fname)
		lname = str(profile.lname)
		username = str(profile.username)
		
		password = generate_password(random.randint(8, 16))
		email = str(profile.email) if profile.email else ''
		user = User.objects.create_user(username, email, password)

		user.is_staff = profile.is_staff
		user.is_superuser = profile.is_superuser		

		user.first_name = fname
		user.last_name = lname
		user.save()

		profile.user = user
		profile.save()


	elif User.objects.filter(username=profile.username).exists():
		user = User.objects.get(username=profile.username)


		if created == False:
			user.username = profile.username
			user.first_name = profile.fname 
			user.last_name = profile.lname
			user.email = str(profile.email) if profile.email else ''

			user.is_staff = profile.is_staff
			user.is_superuser = profile.is_superuser		

			user.save()

		
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