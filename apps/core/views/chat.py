from django.views.generic import TemplateView

class ChatTemplateView(TemplateView):
    template_name = 'index/chat.html'