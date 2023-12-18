from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .models import IP_Address, Profile
from .forms import CustomUserCreationForm
import os

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
def index(request):
	return render(request, 'index.html')

def loginUser(request):

    ipaddr = get_client_ip(request)
    print(ipaddr)

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

            ip = IP_Address.objects.create(user=user, ip=get_client_ip(request))
            ip.save()
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
    ipaddr = get_client_ip(request)

    if request.user.is_authenticated:
        return redirect('index')
    form = CustomUserCreationForm(request.POST or None)
    
    if request.method == 'POST':
        
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False) # Instead of committing data to database, it suspends it temporarily
            user.username = user.username.lower() # Ensures all usernames are lower case to prevent duplicates with different cases.
            user.save() # Finally saves 

            ip = IP_Address.objects.create(user=user, ip=get_client_ip(request))
            ip.save()

            send_mail(
                ('User ' + str(user.username) + ' was successfully created'),
                ('A user was created for brian-lindsay.com!\n\nUsername: ' + str(user.username) + '\n\nName: ' + str(user.first_name) + ' ' + str(user.last_name) + '\n\nEmail: ' + str(user.email) + '\n\n\nThis email is being sent to confirm the creation of accounts. All information on this website is secured and will not be shared with others. This is a portfolio site. I\'m just showcasing what I can do and keeping track of site activity. If you have any questions, you can contact me at the email that sent you this.'),
                'brian.s.lindsay829@gmail.com',
                [str(user.email)],
                fail_silently=False,
            )
            send_mail(
                ('User ' + str(user.username) + ' was successfully created'),
                ('A user was created for brian-lindsay.com!\n\nUsername: ' + str(user.username) + '\n\nName: ' + str(user.first_name) + ' ' + str(user.last_name) + '\n\nEmail: ' + str(user.email) +  "\n\nIP Address: "  + str(ipaddr)),
                'brian.s.lindsay829@gmail.com',
                ['brian.s.lindsay829@gmail.com'],
                fail_silently=False,
            )

            login(request, user) # Logs user in
            return redirect('index')
        else:
            messages.success(request, "An error has occured during registration")

    context = {'form':form, 'site_key':settings.RECAPTCHA_SITE_KEY}
    return render (request, 'accounts/register_account.html', context)

