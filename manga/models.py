from django.db import models

# Create your models here.
def manga(models.Model):
    nombres= models.CharField(max_length=250 )
    descripciones= models.CharField(max_length=500 )
    generos = models.jsonfield(max_length=10)