from django.views.generic import TemplateView


class TeamTemplateView(TemplateView):
    template_name = 'index/team.html'