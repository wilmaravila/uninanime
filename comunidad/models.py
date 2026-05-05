from django.db import models

# Create your models here.
def noticias(models.Model):
    titulo= models.CharField(max_length=500)
    subtitulo= models.CharField(max_length=500)
    etiqueta = models.