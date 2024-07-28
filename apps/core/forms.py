from apps.core.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']