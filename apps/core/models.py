from django.db import models

# Create your models here.
class Costumer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    style =  models.TextField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return "{} {} - Estilo: {}".format(
            self.last_name,
            self.first_name,
            self.style
            
    )
