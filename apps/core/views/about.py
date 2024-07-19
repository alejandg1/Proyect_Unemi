from django.views.generic import TemplateView
from apps.core.mixins import UserGroupMixin

class AboutTemplateView(UserGroupMixin, TemplateView):
    template_name = 'index/about.html'