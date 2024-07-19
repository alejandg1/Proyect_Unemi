from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from apps.security.forms import UserCreationForm, AuthenticationForm
from django.views.generic.base import TemplateView


class LoginView(LoginView):
    form_class = AuthenticationForm
    next_page = reverse_lazy('core:home')
    template_name = 'index/login.html' 

@method_decorator(login_required, name='dispatch') 
class LogoutView(LogoutView):
    next_page = reverse_lazy('core:home')

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'index/register.html'  
    success_url = reverse_lazy('core:home')
    
class NoPermissions(TemplateView):
    template_name = "components/NoPermissions.html"

    

    
