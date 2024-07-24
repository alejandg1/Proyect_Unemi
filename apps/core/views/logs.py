from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django import http


class LoginTemplateView(TemplateView):
    template_name = 'index/login.html'


class NoPermissions(TemplateView):
    template_name = "components/NoPermissions.html"


def Logout(request):
    if request.user.is_temp:
        request.user.delete()
        request.session.flush()
    logout(request)
    return http.HttpResponse("Logged out successfully!")
