from django.db import models
from accounts.models import Profile
import uuid

from django.db.models.deletion import SET_NULL, CASCADE


# Create your models here.
class Post(models.Model):
    
    author = models.ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=30, null=False, blank=False)
    fname = models.CharField(max_length=50, null=False, blank=False)
    lname = models.CharField(max_length=50, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=False, blank=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-created',]

    def save(self, *args, **kwargs):
        self.username = self.author.username
        self.fname = self.author.fname
        self.lname = self.author.lname
        super().save(*args, **kwargs)

    def __str__(self):
        return (f'Post "{self.title}" by {self.username}')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments', null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=CASCADE, related_name="replies", null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=True)
    
    username = models.CharField(max_length=30, null=False, blank=False)
    fname = models.CharField(max_length=50, null=False, blank=False)
    lname = models.CharField(max_length=50, null=False, blank=False)
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    class Meta:
        ordering = ['-created',]
        
    def save(self, *args, **kwargs):
        self.username = self.author.username
        self.fname = self.author.fname
        self.lname = self.author.lname
        super().save(*args, **kwargs)
    
    def __str__(self):
        return (f'Comment by {self.fname} {self.lname}: {self.text}')
    
        
