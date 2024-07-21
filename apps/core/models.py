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


class Image(models.Model):
    Img = models.ImageField(upload_to='images/')
    Type = models.BinaryField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    biography = models.CharField(max_length=1000)
    cv = models.FileField(upload_to='uploads/') 

class Articles(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete= models.CASCADE)
    article_name = models.CharField(max_length=100, null = False)
    
class Projects(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete= models.CASCADE)
    project_name = models.CharField(max_length=100, null = False)
    
class Research(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    research_name = models.CharField(max_length=100, null = False)