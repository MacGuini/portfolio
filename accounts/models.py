from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.functional import empty
import uuid

# Create your models here.

class Profile(models.Model):

	CONTACT_TYPE = (
        ('call', 'Call'),
        ('text', 'Text'),
        ('email', 'Email'),
    )
	# NOTE: fname, lname, and email must be added in any form you create to add a new profile. Built in user model breaks otherwise. Try to figure out solution in signals.
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	username = models.CharField(max_length=100, null=True, blank=True)
	fname = models.CharField(max_length=100, null=True, blank=True)
	lname = models.CharField(max_length=100, null=True, blank=True)
	street1 = models.CharField(max_length=200, null=True, blank=True)
	street2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=2, null=True, blank=True)
	zipcode = models.CharField(max_length=5, null=True, blank=True)

	area1 = models.CharField(max_length=3, null=True, blank=True)
	central1 = models.CharField(max_length=3, null=True, blank=True)
	line1 = models.CharField(max_length=4, null=True, blank=True)

	area2 = models.CharField(max_length=3, null=True, blank=True)
	central2 = models.CharField(max_length=3, null=True, blank=True)
	line2 = models.CharField(max_length=4, null=True, blank=True)

	email = models.EmailField(max_length=200, null=True, blank=True)
	preference = models.CharField(max_length=5, choices=CONTACT_TYPE, default='call', null=True, blank=True)

	created = models.DateTimeField(auto_now_add=True)
	id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)



	def __str__(self):
		return f'{self.fname} {self.lname} - {self.username}'

    