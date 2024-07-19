from django.views.generic import TemplateView
from apps.core.mixins import UserGroupMixin

class ProfileTemplateView(UserGroupMixin, TemplateView):
    template_name = 'index/profile.html'