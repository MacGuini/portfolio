from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm

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

		try:
			user = User.objects.get(username=username)
		except:
			print('\n\n***An error has occured logging in***\n\n')

		user = authenticate(request, username=username, password=password)

		# Makes sure the user exists
		if user is not None:
		
			# creates a session for the users in the database
			login(request, user)

			# returns the user if there is a next route. Otherwise, the user is redirected to the accounts page.
            
			return redirect(request.GET['next'] if 'next' in request.GET else 'index')
			
		else:
			print('Invalid User name or password')

	return render(request, 'accounts/login.html')

def logoutUser(request):
	logout(request)
	return redirect('index')
