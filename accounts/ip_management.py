from accounts.models import IP_Address

def check_ip_exists(ip_address, user):
    ips = IP_Address.objects.filter(user=user)

    for ip in ips:
        
        if ip.ip == ip_address:
            return True
        
    return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
