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
    