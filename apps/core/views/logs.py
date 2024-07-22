from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from apps.core.forms import LoginForm
from django.views.generic.base import TemplateView


class LoginTemplateView(TemplateView):
    template_name = 'index/login.html'


class NoPermissions(TemplateView):
    template_name = "components/NoPermissions.html"
