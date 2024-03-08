from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import IP_Address, Profile
from .forms import CustomUserCreationForm, EmailVerificationForm
from accounts import ip_management, mail_control, validation_control

def verifyEmail(request, pk, token):
    profile = get_object_or_404(Profile, id=pk)

    if token == profile.verification_token:
        print("\n\nVerified\n\n")
        profile.email_valid = True
        profile.save()
        messages.success(request, "Your account has been verified! Welcome " + str(profile.fname) + "!")
        return redirect('verify-success')

    return render(request, 'accounts/login.html')

def newEmailVerification(request):
    form = EmailVerificationForm(request.POST or None)
    if request.method == 'POST':
        # form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                profile = Profile.objects.get(email=email)

                
                newToken = validation_control.generate_token()

                user = profile.user 
                pk = profile.id
                token = newToken
                profile.verification_token = token
                profile.save()
                mail_control.confirmEmail(user, pk, token)
            except Profile.DoesNotExist:
                pass
    return render(request, "accounts/validate_email.html", {"form":form})

# Create your views here.
def index(request):
	return render(request, 'index.html')

def loginUser(request):

    ipaddr = ip_management.get_client_ip(request)


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
            return redirect('login')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Checks if user exists
        if user is not None:
            profile = Profile.objects.get(user=user)

            # Check email validation
            if profile.email_valid:
                ip_exists = ip_management.check_ip_exists(ipaddr, user)  # replace with the IP you want to check
                if not ip_exists:
                    ip = IP_Address.objects.create(user=user, ip=ip_management.get_client_ip(request))
                    ip.save()

                # logs in the user
                login(request, user)
                    
                # returns the user if there is a next route. Otherwise, the user is redirected to the accounts page.
                return redirect(request.GET['next'] if 'next' in request.GET else 'index')
            else:
                # messages.error(request, 'You must validate your email!')
                return redirect(request.GET['next'] if 'next' in request.GET else 'validate-email')
            
        else:
            messages.error(request, 'Invalid username or password')
            # Debugging: Check current messages
            current_messages = messages.get_messages(request)
            for msg in current_messages:
                print(msg)  # or use logging.debug(msg) if print statements don't show up in your environment

            # Ensure not to consume the messages if you plan to display them later
            current_messages.used = False
        
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('index')


def registerUser(request):
    ipaddr = ip_management.get_client_ip(request)

    if request.user.is_authenticated:
        return redirect('index')
    form = CustomUserCreationForm(request.POST or None)
    
    if request.method == 'POST':
        
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False) # Instead of committing data to database, it suspends it temporarily
            user.username = user.username.lower() # Ensures all usernames are lower case to prevent duplicates with different cases.
            user.save() # Finally saves 

            ip_exists = ip_management.check_ip_exists(ipaddr, user)  # replace with the IP you want to check
            if not ip_exists:
                ip = IP_Address.objects.create(user=user, ip=ip_management.get_client_ip(request))
                ip.save()
                

            
            profile = Profile.objects.get(user=user)
            pk = profile.id
            token = profile.verification_token

            mail_control.confirmEmail(user, pk, token)
            mail_control.notifyUserCreated(user, ipaddr)

            return redirect('confirm-email-notice')
        else:
            messages.error(request, "An error has occured during registration")

    context = {'form':form}
    return render (request, 'accounts/register_account.html', context)

