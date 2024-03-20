from django.http import HttpResponseForbidden
from .models import Blacklist
from accounts import mail_control

class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the IP address from the request
        ip_addr = request.META.get('REMOTE_ADDR', None)
        
        # Check if the IP is in the blacklist
        if Blacklist.objects.filter(ip=ip_addr).exists():
            # If the IP is blacklisted, return a forbidden response and sends verification email
            mail_control.blacklistMiddlewareActivated(ip_addr)
            return HttpResponseForbidden('Access denied.')

        # If the IP is not blacklisted, proceed with the request
        response = self.get_response(request)
        
        return response
