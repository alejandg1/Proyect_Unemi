from django.views.generic import TemplateView
from pathlib import Path
from django.shortcuts import render as Render
import os
from django.conf import settings
from PIL import Image
from django.shortcuts import redirect
from apps.core.models import User, GeneratedImage


class CollageTemplateView(TemplateView):
    template_name = 'index/collage.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
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


def collage_pill(group_img):
    images = []
    UnemiIMG = Image.open(os.path.join(settings.MEDIA_ROOT, 'unemi.png'))
    for img in group_img:
        url = f'{settings.BASE_DIR}{img}'
        images.append(Image.open(url))
    countFiles = os.listdir(os.path.join(settings.MEDIA_ROOT, 'collages'))
    collageURL = os.path.join(
        settings.MEDIA_ROOT, 'collages', f'collage{len(countFiles)+1}.png')
    collage_W = max([img.width for img in images])*4
    collage_H = sum([img.height for img in images])*3
    collage = Image.new('RGB', (collage_W, collage_H))
    centralPosition = (collage_W//4, collage_H//3)
    collage.paste(UnemiIMG, centralPosition)
    positions = [(x*collage_W//4, y*collage_H//3)
                 for x in range(4) for y in range(3)]
    for img, pos in zip(images, positions):
        collage.paste(img, pos)
    collage.save(collageURL)
    return collageURL


def MakeCollage(request):
    users = User.objects.filter(is_temp=True)
    images = GeneratedImage.objects.filter(user__in=users)
    grupos = []
    grupos = separar_imagenes(images)
    superusers = User.objects.filter(is_superuser=True)
    collages = []
    for group in grupos:
        NewCollage = collage_pill(group)
        collages.append(NewCollage)
        for user in superusers:
            GeneratedImage.objects.create(user=user, Img=NewCollage)
    return Render(request, 'index/collage.html', {'collages': collages})
