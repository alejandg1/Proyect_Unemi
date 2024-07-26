from django.views.generic import TemplateView
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
        max = 14
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
    try:
        images = []
        WT, HG = 250, 240
        rows, cols = 3, 5
        UnemiIMG = Image.open(os.path.join(settings.MEDIA_ROOT, 'unemi.png'))
        UnemiIMG = UnemiIMG.resize((WT, HG))
        countFiles = os.listdir(os.path.join(
            settings.MEDIA_ROOT, 'collages'))
        collageURL = os.path.join(settings.MEDIA_ROOT,
                                  'collages', f'collage{
                                      len(countFiles)+1}.png')

        positions = [(x * WT, y * HG)
                     for y in range(rows) for x in range(cols)]
        for img in group_img:
            url = f'{settings.BASE_DIR}{img}'
            images.append(Image.open(url).resize((WT, HG)))
        collage_W = 320 * cols
        collage_H = 240 * rows
        collage = Image.new('RGB', (collage_W, collage_H), (255, 255, 255))
        if len(images) < 7:
            next = ()
            for img, pos in zip(images, positions):
                collage.paste(img, pos)
                next = positions.index(pos)
            print(next+1)
            collage.paste(UnemiIMG, positions[next+1])
        else:
            for img, pos in zip(images, positions):
                if pos == (640, 240):
                    collage.paste(UnemiIMG, pos)
                else:
                    collage.paste(img, pos)

        collage.save(collageURL)
        return collageURL

    except Exception as e:
        print("pill=>", e)
        return None


def MakeCollage(request):
    try:
        users = User.objects.filter(is_temp=True)
        images = GeneratedImage.objects.filter(user__in=users)
        grupos = []
        grupos = separar_imagenes(images)
        superusers = User.objects.filter(is_superuser=True)
        collages = []
        for group in grupos:
            if len(group) > 0:
                NewCollage = collage_pill(group)
                collages.append(NewCollage)
            for user in superusers:
                GeneratedImage.objects.create(user=user, Img=NewCollage)
        return Render(request, 'index/collage.html', {'collages': collages})
    except Exception as e:
        print("mkcol=>", e)
        return Render(request, 'index/collage.html', {'collages': []})
