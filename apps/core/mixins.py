from django.http import HttpResponseRedirect
from django.contrib import messages
from apps.security.models import User
from django.http import Http404
from django.shortcuts import render

class UserGroupMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_permissions = self.request.user.get_all_permissions()
        context['permissions'] = list(all_permissions)
        return context
    
class NoPermissionMixin(object):
    login_url = '/withoutpermissions/'
    permission_denied_message = "No tienes los permisos necesarios para ver está página"
    raise_exception = False
    
    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.login_url)
    
class UpdateMixin(object):
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        
        except Http404:
            return render(request, 'components/http404.html')
        
    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario: verifica los datos.')
        return super().form_invalid(form)

class DeleteMixin(object):
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        
        except Http404:
            return render(request, 'components/http404.html')