from django.views.generic.base import TemplateView
from apps.core.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.forms import LoginForm


class LoginTemplateView(LoginView):
    form_class = LoginForm
    template_name = 'index/login.html'
    next_page = reverse_lazy('core:home')


class NoPermissions(TemplateView):
    template_name = "components/NoPermissions.html"


def DelTemps(request):
    users = User.objects.filter(is_temp=True)
    for user in users:
        user.delete()
