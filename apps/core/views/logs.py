from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django import http
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.forms import LoginForm

class LoginTemplateView(LoginView):    
    form_class = LoginForm
    template_name = 'index/login.html'
    next_page = reverse_lazy('core:home')

class NoPermissions(TemplateView):
    template_name = "components/NoPermissions.html"


def Logout(request):
    if request.user.is_temp:
        request.user.delete()
        request.session.flush()
    logout(request)
    return http.HttpResponse("Logged out successfully!")
