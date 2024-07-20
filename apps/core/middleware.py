from django.contrib.auth import login, logout
from django.utils.deprecation import MiddlewareMixin
from apps.core.models import User


class TemporaryUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            username = User.objects.count() + 1
            temp_user = User.objects.create_user(
                username=f'temp_{username}', is_temp=True)

            login(request, temp_user)

    def process_response(self, request, response):
        if request.user.is_authenticated and request.user.is_temp and not request.session.exists(request.session.session_key):
            logout(request)
            request.user.is_active = False
            request.user.delete()
        return response
