from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone
import uuid
from accounts import validation_control

# Create your models here.

class Profile(models.Model):

	CONTACT_TYPE = (
		('', 'None'), 
        ('home', 'Home'),
		('mobile', 'Mobile'),
		('work', 'Work'),
        ('text', 'Text'),
        ('email', 'Email'),
    )
	# NOTE: fname, lname, and email must be added in any form you create to add a new profile. Built in user model breaks otherwise. Try to figure out solution in signals.
	user = models.OneToOneField(User, on_delete=CASCADE, null=True, blank=True)
	username = models.CharField(max_length=30, null=True, blank=True, unique=True)
	fname = models.CharField(max_length=50, null=True, blank=True)
	mname = models.CharField(max_length=50, null=True, blank=True)
	lname = models.CharField(max_length=50, null=True, blank=True)
	street1 = models.CharField(max_length=100, null=True, blank=True)
	street2 = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	state = models.CharField(max_length=2, null=True, blank=True)
	zipcode = models.CharField(max_length=5, null=True, blank=True)

	home = models.CharField(max_length=10, null=True, blank=True)
	mobile = models.CharField(max_length=10, null=True, blank=True)
	work = models.CharField(max_length=10, null=True, blank=True)

	email = models.EmailField(max_length=200, null=True, blank=True, unique=True)
	preference = models.CharField(max_length=6, choices=CONTACT_TYPE, default='home', null=True, blank=True)

	verification_token = models.CharField(max_length=100, blank=True, null=True)
	token_created_at = models.DateTimeField(null=True, blank=True)

	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	is_approved = models.BooleanField(default=False)
	email_valid = models.BooleanField(default=False)
	

	created = models.DateTimeField(auto_now_add=True)
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)



	def __str__(self):
		return f'{self.fname} {self.lname} - {self.username}'
	
	def save(self, *args, **kwargs):
		if not self.verification_token:
			self.verification_token = validation_control.generate_token()
			self.token_created_at = timezone.now()
		super(Profile, self).save(*args, **kwargs)
	
class IP_Address(models.Model):
	user = models.ForeignKey(User, on_delete=CASCADE, null=False, blank=False)
	ip = models.GenericIPAddressField(editable=False)

	created = models.DateTimeField(auto_now_add=True, editable=False)
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

	def __str__(self):
		return f"{self.user} logged in from {self.ip} on {self.created}"

class Blacklist(models.Model):
	ip = models.GenericIPAddressField(editable=False)

	created = models.DateTimeField(auto_now_add=True, editable=False)
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

	def __str__(self):
		return f"IP Address: {self.ip}"