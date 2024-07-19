from django.views.generic import TemplateView
from apps.core.mixins import UserGroupMixin

class HomeTemplateView(UserGroupMixin, TemplateView):
    template_name = 'index/home.html'

