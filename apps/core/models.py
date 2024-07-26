from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_temp = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = ("Usuario")
        verbose_name_plural = ("Usuarios")

    def __str__(self):
        return "Usuario: {}".format(self.username)


class GeneratedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Img = models.ImageField(upload_to='generated/')

    def delete(self, *args, **kwargs):

        if self.Img:
            self.Img.delete(save=False)

        super(GeneratedImage, self).delete(*args, **kwargs)


class AcademicD (models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

    def delete(self, *args, **kwargs):
        super(AcademicD, self).delete(*args, **kwargs)


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images/')
    cargo = models.CharField(max_length=100, null=True, blank=True)
    titles = models.ManyToManyField(AcademicD)
    f_init = models.DateField(null=True, blank=True)
    f_end = models.DateField(null=True, blank=True)
    biography = models.CharField(
        max_length=1000, null=True, blank=True, default=None)
    cv = models.FileField(upload_to='uploads/',
                          default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'image': self.img.url if self.img else None,
            'name': self.name,
            'bio': self.biography,
            'cv': self.cv.url if self.cv else None
        }

    def delete(self, *args, **kwargs):

        if self.img:
            self.img.delete(save=False)

        super(Teacher, self).delete(*args, **kwargs)


class Articles(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    article_name = models.CharField(max_length=100, null=False)
    url = models.URLField(default='#', null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.teacher.name, self.article_name)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'teacher_id': self.teacher.id,
            'article_name': self.article_name
        }


class Projects(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100, null=False)
    url = models.URLField(default='#', null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.teacher.name, self.project_name)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'teacher_id': self.teacher.id,
            'project_name': self.project_name
        }


class Research(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    research_name = models.CharField(max_length=100, null=False)
    url = models.URLField(default='#', null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.teacher.name, self.research_name)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'teacher_id': self.teacher.id,
            'research_name': self.research_name
        }


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    img = models.ImageField(upload_to='team/')
    description = models.TextField(null=True)

    def delete(self, *args, **kwargs):

        if self.img:
            self.img.delete(save=False)

        super(Team, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name
