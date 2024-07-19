from django.views.generic import TemplateView
from apps.core.mixins import UserGroupMixin, NoPermissionMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

class OptionsTemplateView(UserGroupMixin, NoPermissionMixin, LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'management_options.html'
    permission_required = 'security.view_user'