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
        max = 13
        for i in range(0, len(images), max):
            grupo = []
            for j in range(i, min(i + max, len(images))):
                grupo.append(images[j].Img.url)
            grupos.append(grupo)
        return grupos
    except Exception as e:
        print(e)


def collage_pill(group_img):
    try:
        images = []
        WT, HG = 305, 240
        rows, cols = 3, 5
        margin = 5
        UnemiIMG = Image.open(os.path.join(settings.MEDIA_ROOT, 'unemi.jpeg'))
        UnemiIMG = UnemiIMG.resize((320, 240))
        countFiles = os.listdir(os.path.join(
            settings.MEDIA_ROOT, 'collages'))
        collageName = f'collage{len(countFiles)+1}.png'
        collageURL = os.path.join(settings.MEDIA_ROOT,
                                  'collages', f'collage{
                                      len(countFiles)+1}.png')

        positions = [(x * WT+margin, y * HG+margin)
                     for y in range(rows) for x in range(cols)]
        for img in group_img:
            url = f'{settings.BASE_DIR}{img}'
            images.append(Image.open(url).resize((WT, HG)))
        collage_W = (WT+margin) * cols
        collage_H = (HG+margin) * rows
        collage = Image.new('RGB', (collage_W, collage_H), (137, 137, 127))
        if len(images) < 7:
            next = ()
            for img, pos in zip(images, positions):
                collage.paste(img, pos)
                next = positions.index(pos)
            collage.paste(UnemiIMG, positions[next+1])
        else:
            for img, pos in zip(images, positions):
                if pos == (615, 245):
                    collage.paste(UnemiIMG, pos)
                else:
                    collage.paste(img, pos)

        collage.save(collageURL)
        return collageName

    except Exception as e:
        print("pill=>", e)
        return None


def MakeCollage(request):
    images = []
    try:
        users = User.objects.filter(is_temp=True)
        images = GeneratedImage.objects.filter(user__in=users)
        grupos = []
        grupos = separar_imagenes(images)
        superusers = User.objects.filter(is_superuser=True)
        collages = []
        names = []
        for group in grupos:
            if len(group) > 0:
                name = collage_pill(group)
                if name is not None:
                    collages.append(f'{settings.MEDIA_URL}collages/{name}')
                    names.append(name)

                for user in superusers:
                    GeneratedImage.objects.create(
                        user=user, Img=f'{settings.MEDIA_URL}collages/{name}')
    except Exception as e:
        print("mkcol=>", e)
    return Render(request, 'index/collage.html', {'collages': collages})


def Delete_collages(request):
    try:
        images = GeneratedImage.objects.filter(Img__contains='collage')
        for img in images:
            if os.path.exists(f'{settings.MEDIA_ROOT}{img.Img}'):
                os.remove(f'{settings.MEDIA_ROOT}{img.Img}')
            img.delete()
        return redirect('core:collage')
    except Exception as e:
        print("delete=>", e)
        return redirect('core:collage')
