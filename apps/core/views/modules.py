from django.views.generic import TemplateView
from apps.core.mixins import UserGroupMixin

class ModulesTemplateView(UserGroupMixin, TemplateView):
    template_name = 'index/modules.html'
