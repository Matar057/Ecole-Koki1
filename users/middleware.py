from django.conf import settings
from django.utils import timezone
import zoneinfo


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'timezone'):
            tz_name = request.user.timezone or settings.TIME_ZONE
        else:
            tz_name = settings.TIME_ZONE
        try:
            timezone.activate(zoneinfo.ZoneInfo(tz_name))
        except Exception:
            timezone.activate(zoneinfo.ZoneInfo('UTC'))
        return self.get_response(request)
