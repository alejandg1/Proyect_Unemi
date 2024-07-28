from django.views.generic import TemplateView
from apps.core.models import Team

class TeamTemplateView(TemplateView):
    template_name = 'index/team.html'
    team = Team.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.team
        return context