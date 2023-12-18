from django.contrib import admin
from .models import Profile, IP_Address

# Register your models here.

admin.site.register(Profile)
admin.site.register(IP_Address)