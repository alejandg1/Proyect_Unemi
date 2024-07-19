from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from apps.security.models import User
from django import forms


class AuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = list(UserCreationForm.Meta.fields) + ['profile_picture', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        
class UserCreateForm(UserChangeForm):
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput,
        required=True,
        help_text=(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = '__all__'
        
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ('password', 'Password', )
