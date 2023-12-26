from django.conf import settings

def site_key(request):
    return {'site_key':settings.RECAPTCHA_SITE_KEY}