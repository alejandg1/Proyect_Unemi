from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings

class User(AbstractUser):
  dni = models.CharField(verbose_name='Cédula o RUC', max_length=13, blank=True,null=True)
  profile_picture = models.ImageField(("Imagen de perfil"), upload_to='profile_pics/', null=True, blank=True)
  email = models.EmailField(("Email"), unique=True, max_length=254)
  direction=models.CharField('Direccion',max_length=200,blank=True,null=True)
  phone=models.CharField('Telefono',max_length=50,blank=True,null=True)
  groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_groups'
    )
  
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username", "first_name", "last_name"]
  
  class Meta:
    verbose_name = ("Usuario")
    verbose_name_plural = ("Usuarios")
  
  def __str__(self):
      return "{} - Email: {}".format(self.username, self.email)
  
  
  def save(self, *args, **kwargs):
    is_new_user = not self.pk
    super().save(*args, **kwargs)  
    
    if is_new_user:
        group, created = Group.objects.get_or_create(name='User')
        self.groups.add(group)
    
  def get_image_url(self):
    if self.profile_picture:
        return '{}{}'.format(settings.MEDIA_URL, self.profile_picture)
      
    else:
        return '/static/images/perfil.jpg'

