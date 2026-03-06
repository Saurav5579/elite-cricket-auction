from django.shortcuts import redirect
from .models import SiteSetting

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings_obj = SiteSetting.objects.first()

        if settings_obj and settings_obj.maintenance_mode:
            if not request.path.startswith('/admin'):
                return redirect('maintenance_page')

        return self.get_response(request)