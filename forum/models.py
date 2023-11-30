from django.db import models
from accounts.models import Profile
import uuid

from django.db.models.deletion import SET_NULL


# Create your models here.
class Post(models.Model):
    
    user = models.ForeignKey(Profile, on_delete=SET_NULL, null=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    fname = models.CharField(max_length=100, null=True, blank=True)
    lname = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
