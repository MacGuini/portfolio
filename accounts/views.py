import logging
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import requests
from .models import IP_Address, Profile, Blacklist
from .forms import CustomUserCreationForm, EmailVerificationForm, BlacklistForm, ProfileForm
from accounts import ip_management, mail_control, validation_control


logger = logging.getLogger(__name__)

@login_required(login_url='login')
def blacklistIP(request):
    if request.method == "POST":
        form = BlacklistForm(request.POST)
        if form.is_valid():
            selected_ips = form.cleaned_data['ip_address']
            for ip_address in selected_ips:
                Blacklist.objects.get_or_create(ip=ip_address.ip)
            return redirect('index')
    else:
        form = BlacklistForm()
    
    return render(request, 'accounts/blacklist.html', {'form':form})

def blacklisted(request):
    logout(request)
    ipaddr = ip_management.get_client_ip(request)
    mail_control.blacklistBlocked(ipaddr)

    return render(request, 'accounts/blacklisted.html')

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

    ipaddr = ip_management.get_client_ip(request)

    # Checks if user is blacklisted and prevents login
    blacklisted = Blacklist.objects.filter(ip=ipaddr).exists()

    if blacklisted:
        logout(request)
        logger.info("Index blocked: blacklisted IP %s", ipaddr)
        return redirect('blacklisted')
    else:
	    return render(request, 'index.html')


def loginUser(request):

    ipaddr = ip_management.get_client_ip(request)

    # Checks if user is blacklisted and prevents login
    blacklisted = Blacklist.objects.filter(ip=ipaddr).exists()

    if blacklisted:
        logger.info("Login blocked: blacklisted IP %s", ipaddr)
        return redirect('blacklisted')
    
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST' and not blacklisted:
        
        # Username forced lower case to prevent repeat users
        username = request.POST['username'].lower()
        password = request.POST['password']

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
            logger.info("Login attempt for user %s", username)
        except User.DoesNotExist:
            logger.error("Login failed: user %s does not exist", username)
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
                messages.error(request, 'You must validate your email!')
                logger.info("Login blocked: user %s email not validated", username)
                return redirect(request.GET['next'] if 'next' in request.GET else 'validate-email')
            
        else:
            messages.error(request, 'Invalid username or password')
            logger.error("Login failed: invalid credentials for user %s", username)
            # Debugging: Check current messages
            current_messages = messages.get_messages(request)
            for msg in current_messages:
                logger.debug("Current message: %s", msg)

            # Ensure not to consume the messages if you plan to display them later
            current_messages.used = False
        
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('index')


def registerUser(request):
    ipaddr = ip_management.get_client_ip(request)

    # Checks if user is blacklisted and prevents login
    blacklisted = Blacklist.objects.filter(ip=ipaddr).exists()

    if blacklisted:
        logger.info("Register blocked: blacklisted IP %s", ipaddr)
        return redirect('blacklisted')
    
    if request.user.is_authenticated:
        return redirect('index')
    
    form = CustomUserCreationForm(request.POST or None)
    
    if request.method == 'POST' and not blacklisted:
        
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY_V2,
            'response': recaptcha_response
        }
        try:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
        except Exception as e:
            logger.exception("reCAPTCHA verify request failed")
            messages.error(request, "Captcha verification error. Try again.")
            mail_control.captchaFail()
            return render(request, 'accounts/register_account.html', {'form': form})

        # Checks to ensure only certain hosts are allowed to sign up.
        email_allowed = False # Default to False
        email = request.POST.get('email').lower()
        allowed_domains = ['gmail.com','yahoo.com','hotmail.com','outlook.com','aol.com','icloud.com']
        domain = email.split('@')[1]

        # 1st email check point verifies if email is allowed by domain
        if domain not in allowed_domains:
            email_allowed=False
            messages.error(request, "You cannot use that domain for your email.")
            logger.info("Register blocked: disallowed email domain %s", domain)
        else:
            email_allowed=True
            logger.info("Register allowed: email domain %s", domain)

        # 2nd email checkpoint verifying unique email was used
        if User.objects.filter(email=email).exists():
            email_allowed=False
            messages.error(request, "Email already in use.")
            logger.info("Register blocked: email already in use %s", email)

        form = CustomUserCreationForm(request.POST)
        if result.get('success'):
                
            if form.is_valid() and email_allowed:
                
                user = form.save(commit=False) # Instead of committing data to database, it suspends it temporarily
                user.username = user.username.lower() # Ensures all usernames are lower case to prevent duplicates with different cases.
                user.save() # Finally saves
                logger.info("Register success: user=%s ip=%s", user.username, ipaddr)

                if not ip_management.check_ip_exists(ipaddr, user):  # replace with the IP you want to check:
                    ip = IP_Address.objects.create(user=user, ip=ip_management.get_client_ip(request))
                    ip.save()
                    logger.info("IP address %s saved for user %s", ipaddr, user.username)
                    

                
                profile = Profile.objects.get(user=user)
                pk = profile.id
                token = profile.verification_token
                logger.info("Sending confirmation email to user %s with token %s", user.username, token)

                mail_control.confirmEmail(user, pk, token)
                mail_control.notifyUserCreated(user, ipaddr)

                return redirect('confirm-email-notice')
            else:
                messages.error(request, "An error has occured during registration")
                logger.error(
                    "Register failed: email_allowed=%s | user=%s | email=%s | domain=%s | form_errors=%s",
                    email_allowed,
                    request.POST.get('username', 'unknown'),
                    request.POST.get('email', 'unknown'),
                    request.POST.get('email', 'unknown').split('@')[1] if '@' in (request.POST.get('email') or '') else '',
                    form.errors.as_json()  # or just form.errors if you prefer brevity
                )
        else:
            logger.info("Register blocked: reCAPTCHA failed for user %s", request.POST.get('username', 'unknown'))
            messages.error(request, 'Please complete recaptcha challenge')
            mail_control.captchaFail()
    context = {'form':form}
    return render (request, 'accounts/register_account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user # Ensure user is attached 
            obj.save()
            messages.success(request, "Account updated successfully!")
            return redirect('edit-account')
        else:
            messages.error(request, "An error has occurred during update.")
    
    return render(request, 'accounts/edit_account.html', {'form': form})
