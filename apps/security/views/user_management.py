from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from apps.core.mixins import NoPermissionMixin, UserGroupMixin, UpdateMixin, DeleteMixin
from apps.security.models import User
from apps.security.forms import UserCreateForm, UserUpdateForm

class UserListView(UserGroupMixin, NoPermissionMixin, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'options/user.html'
    permission_required = 'security.view_user'
    context_object_name = 'userlist'
    paginate_by = 2
    
    def get_queryset(self):
        query = self.request.GET.get('query')

        if query:
            queryset = self.model.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
            print(f"Filtered QuerySet: {self.model.objects.all()}")
            return queryset.order_by('id')
        
        else:
            print(f"Filtered QuerySet: {self.model.objects.all()}")
            return self.model.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de usuarios/empleados'
        context['button'] = 'usuario'
        # context['create_url'] = reverse_lazy('security:user_create')
        context['headers'] = [
            'Imagen de perfil',
            'Usuario', 
            'Nombres',
            'Apellidos',
            'Email',
            'Acciones'
            ]
        return context
        
class UserCreateView(UserGroupMixin, NoPermissionMixin, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    template_name = 'options/new_user.html'
    permission_required = 'asistencia.add_user'
    form_class = UserCreateForm
    success_url = reverse_lazy('security:user')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Ingresar nuevo usuario/empleado'
        context['list'] = reverse('security:user')
        return context
    
    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)
    
class UserUpdateView(UserGroupMixin, NoPermissionMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateMixin, UpdateView):
    model = User
    template_name = 'options/new_user.html'
    permission_required = 'security.change_user'
    form_class = UserUpdateForm
    success_url = reverse_lazy('security:user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Actualizar usuario/empleado'
        context['list'] = reverse('security:user')
        return context
    
class UserDeleteView(UserGroupMixin, NoPermissionMixin, LoginRequiredMixin, PermissionRequiredMixin, DeleteMixin, DeleteView):
    model = User
    template_name = 'options/delete_user.html'
    permission_required = 'security.delete_user'
    success_url = reverse_lazy('security:user')
    context_object_name = 'current_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Eliminar usuario'
        context['list'] = reverse('security:user')
        return context