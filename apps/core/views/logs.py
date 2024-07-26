from django.views.generic.base import TemplateView
from django import http
from django.shortcuts import redirect
from apps.core.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from apps.core.forms import LoginForm


class LoginTemplateView(LoginView):
    form_class = LoginForm
    template_name = 'index/login.html'
    next_page = reverse_lazy('core:collage')


class NoPermissions(TemplateView):
    template_name = "components/NoPermissions.html"


def DelTemps(request):
    try:

        users = User.objects.filter(is_temp=True)
        for user in users:
            user.delete()
        return redirect('core:collage')
    except:
        return http.HttpResponseServerError("Error")


def Logout(request):
    request.session.flush()
    return redirect('core:home')
