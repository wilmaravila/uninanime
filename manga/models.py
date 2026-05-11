#Libreria para crear errores manuales
from django.core.exceptions import ValidationError

from django.db import models

#Estructura para creacion del enum
class EstadoManga(models.TextChoices):
    EMISION= 'EM','En emision'
    FINALIZADO = 'FI', 'Finalizado'
    PAUSA = 'PA', 'En pausa'

# Funcion de validacion de estructura de la review 
def validador_review(value):
    if not isinstance(value,list):
        raise ValidationError(
            "review debe ser una lista"
        )
    for review in value:
        estruc_review =[
            "user_id",
            "username",
            "comment"
        ]
        for parametro in estruc_review:
            if parametro not in review:
                raise ValidationError(
                    f"falta el campo{parametro}"
                )

#Modelo necesario para crear un manga 
class Manga(models.Model):
    titulo= models.CharField(max_length=250 )
    descripcion= models.TextField()
    generos = models.JSONField(default=list)
    capitulos = models.IntegerField()
    estado = models.CharField(max_length=2, choices= EstadoManga.choices, default= EstadoManga.EMISION)
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    review = models.JSONField(default=list, validators=[validador_review])
    def __str__(self):
        return self.titulo


class Autor(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    def __str__(self):
        return self.nombre
