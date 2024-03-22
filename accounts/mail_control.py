from django.core.mail import send_mail

def notifyUserCreated(user, ipaddr):
    send_mail(
    ('User ' + str(user.username) + ' was successfully created'),
    ('A user was created for brian-lindsay.com!\n\nUsername: ' + str(user.username) + '\n\nName: ' + str(user.first_name) + ' ' + str(user.last_name) + '\n\nEmail: ' + str(user.email) +  "\n\nIP Address: "  + str(ipaddr)),
    'brian.s.lindsay829@gmail.com',
    ['brian.s.lindsay829@gmail.com'],
    fail_silently=False,
) 

def confirmEmail(user, pk, token):

    send_mail(
        ('User ' + str(user.username) + ' was successfully created'),
        ('A user was created for brian-lindsay.com!\n\nUsername: ' + str(user.username) + '\n\nName: ' + str(user.first_name) + ' ' + str(user.last_name) + '\n\nEmail: ' + str(user.email) + "\n\n\nThis email is being sent to confirm the creation of accounts. All information on this website is secured and will not be shared with others. This is a portfolio site. I'm just showcasing what I can do and keeping track of site activity. If you have any questions, you can contact me at the email that sent you this.\n\n\nBefore you can log on, you must first verify your email. Click or copy and paste this link to verify. https://brian-lindsay.com/verify-email/"+str(pk)+ "/"+ str(token) + "/"),
        'brian.s.lindsay829@gmail.com',
        [str(user.email)],
        fail_silently=False,
    )

def blacklistBlocked(ipaddr):
    send_mail(
        (f'Blacklist blocked IP Address: {ipaddr}'),
        (f'This message sent to alert you that the IP blocker has successfully blocked a request from {ipaddr}'),
        'brian.s.lindsay829@gmail.com',
        ['brian.s.lindsay829@gmail.com'],
        fail_silently=False
    )

def blacklistMiddlewareActivated(ipaddr):
    send_mail(
        f'Blacklist Middleware activated, blocking {ipaddr}',
        f'This email was sent to verify that the middleware blacklisting is functioning correctly. The IP address {ipaddr} has been blocked.',
        'brian.s.lindsay829@gmail.com',
        ['brian.s.lindsay829@gmail.com'],
        fail_silently=False
    )
def captchaFail():
    send_mail(
        f'Captcha failed',
        f'Someone failed the captcha test on brian-lindsay.com',
        'brian.s.lindsay829@gmail.com',
        ['brian.s.lindsay829@gmail.com'],
        fail_silently=False
    )