from django.contrib.auth import login
from django.utils.deprecation import MiddlewareMixin
from apps.core.models import User


class TemporaryUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            username = User.objects.count() + 1
            temp_user = User.objects.create_user(
                username=f'temp_{username}', is_temp=True)

            login(request, temp_user)
#         # if request.user.is_authenticated and request.user.is_temp and not request.session.exists(request.session.session_key):
#         #     logout(request)
#         #     request.user.is_active = False
#         #     request.user.delete()
#
#
# class SessionExpiryMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.session.get('has_expired', False):
#             print('Session has expired')
#             logout(request)
#             request.user.is_active = False
#             request.user.delete()
#             del request.session['has_expired']
#
#         if not request.session.exists(request.session.session_key):
#             request.session['has_expired'] = True
