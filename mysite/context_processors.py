from django.conf import settings

def site_key(request):
    return {'site_key':settings.RECAPTCHA_SITE_KEY}


def recaptcha_v2_key(request):
    return {'site_key':settings.RECAPTCHA_SITE_KEY_V2}
