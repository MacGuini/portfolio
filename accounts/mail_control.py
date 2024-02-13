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
        ('A user was created for brian-lindsay.com!\n\nUsername: ' + str(user.username) + '\n\nName: ' + str(user.first_name) + ' ' + str(user.last_name) + '\n\nEmail: ' + str(user.email) + "\n\n\nThis email is being sent to confirm the creation of accounts. All information on this website is secured and will not be shared with others. This is a portfolio site. I'm just showcasing what I can do and keeping track of site activity. If you have any questions, you can contact me at the email that sent you this.\n\n\nBefore you can log on, you must first verify your email. Click or copy and paste this link to verify. http://127.0.0.1:8000/verify-email/"+str(pk)+ "/"+ str(token) + "/"),
        'brian.s.lindsay829@gmail.com',
        [str(user.email)],
        fail_silently=False,
    )