from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import LoginForm
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
        
    return render(request, 'accounts/login.html')

# def loginUser(request):
    
#     if request.user.is_authenticated:
#         return redirect('index')

#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # Username forced lower case to prevent repeat users
#             username = request.POST['username'].lower()
#             password = request.POST['password']

#             # Check if the user exists
#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 messages.error(request, 'User does not exist.')
#                 return render(request, 'accounts/login.html', {'form':form})

#             # Authenticate the user
#             user = authenticate(request, username=username, password=password)

#             # Checks if user exists
#             if user is not None:

#                 # creates a session for the users in the database
#                 login(request, user)
                    
#                 # returns the user if there is a next route. Otherwise, the user is redirected to the accounts page.
#                 return redirect(request.GET['next'] if 'next' in request.GET else 'index')

#             else:
#                 messages.error(request, 'Invalid password')
            
            
#     else:
#         form = LoginForm()

#     return render(request, 'accounts/login.html', {'form':form})


def logoutUser(request):
	logout(request)
	return redirect('index')
