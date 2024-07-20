from django.views.generic import TemplateView


class ProfileTemplateView(TemplateView):
    template_name = 'index/profile.html'
