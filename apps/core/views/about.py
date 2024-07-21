from django.views.generic import TemplateView
from django.views import View
from apps.core.models import Teacher, Projects, Research, Articles
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

class AboutTemplateView(TemplateView):
    teachers = Teacher.objects.all()
    template_name = 'index/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = self.teachers
        print(self.teachers)
        return context

class TeacherDataResponse(View):
    def post(self, request, *args, **kwargs):
        
        data = json.loads(request.body)
        teacher_id = data['teacher_id']
        print(teacher_id)
        
        teacher = Teacher.objects.get(id = teacher_id) 
        
        if teacher is None:
            
            return JsonResponse({
            'success': False
            })
            
        projects = Projects.objects.filter(teacher = teacher)
        if projects:
            projects = [project.to_dict() for project in projects]
        print(projects)
        
        articles = Articles.objects.filter(teacher = teacher)
        if articles:
            articles = [article.to_dict() for article in articles]
        print(articles)
        
        research = Research.objects.filter(teacher = teacher)
        if research:
            research = [research.to_dict() for research in research]
        print(research)
        
        data = {   
                'success': True, 
                'projects': projects if projects else None,
                'articles': articles if articles else None,
                'research': research if research else None
            }
        
        print(data)

        return JsonResponse(data)
        