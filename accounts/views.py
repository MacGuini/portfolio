from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm
import os

# Create your views here.
def index(request):
	return render(request, 'index.html')

def loginUser(request):
    
    if request.user.is_authenticated:
        return redirect('index')
    

    if request.method == 'POST':
        
        # Username forced lower case to prevent repeat users
        username = request.POST['username'].lower()
        password = request.POST['password']

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Checks if user exists
        if user is not None:

            # creates a session for the users in the database
            login(request, user)
                
            # returns the user if there is a next route. Otherwise, the user is redirected to the accounts page.
            return redirect(request.GET['next'] if 'next' in request.GET else 'index')

        else:
            messages.error(request, 'Invalid password')
        
    return render(request, 'accounts/login.html', {'site_key':settings.RECAPTCHA_SITE_KEY})


@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('index')

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = CustomUserCreationForm(request.POST or None)
    
    if request.method == 'POST':
        
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False) # Instead of committing data to database, it suspends it temporarily
            user.username = user.username.lower() # Ensures all usernames are lower case to prevent duplicates with different cases.
            user.save() # Finally saves 
            
            login(request, user) # Logs user in
            return redirect('index')
        else:
            messages.success(request, "An error has occured during registration")

    context = {'form':form, 'site_key':settings.RECAPTCHA_SITE_KEY}
    return render (request, 'accounts/register_account.html', context)

