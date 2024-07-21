from apps.core.models import User
from django import forms


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
