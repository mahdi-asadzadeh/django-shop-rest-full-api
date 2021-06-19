from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache


class OnlineUserNowMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check the IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        # Get the list of the latest online users
        # online = cache.get_many("online_now").keys()
        online = cache.get('online_now')
        # Check the active IP addresses
        if online:
            online = [ip for ip in online if cache.get(ip)]
        else:
            online = []
        # Add the new IP to cache
        cache.set(user_ip, user_ip, 600)
        # Add the new IP to list if doesn't exist
        if user_ip not in online:
            online.append(user_ip)
        # Set the new online list
        cache.set('online_now', online)
        # Add the number of online users to request
        request.__class__.online_now = len(online)

