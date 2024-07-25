from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from apps.core.models import User, GeneratedImage


class CollageTemplateView(TemplateView):
    template_name = 'index/collage.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:home')
        else:
            return super().get(request, *args, **kwargs)


def separar_imagenes(images):
    try:
        grupos = []
        max = 10
        used = 0
        for i in images:
            grupo = []
            if used <= len(images):
                if max > len(images):
                    max = len(images)
                for j in range(used, max):
                    grupo.append(images[j].Img.url)
                    used += 1
            grupos.append(grupo)
        return grupos
    except Exception as e:
        print(e)


def MakeCollage(request):
    users = User.objects.filter(is_temp=True)
    images = GeneratedImage.objects.filter(user__in=users)
    grupos = []
    grupos = separar_imagenes(images)
    print(grupos)
    return JsonResponse({'images': grupos})
