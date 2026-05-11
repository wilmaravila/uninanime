#Libreria para crear errores manuales
from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import models
import uuid

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
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    titulo= models.CharField(max_length=250 )
    descripcion= models.TextField()
    poster_url = models.URLField()
    generos = models.JSONField(default=list)
    capitulos = models.IntegerField()
    estado = models.CharField(max_length=2, choices= EstadoManga.choices, default= EstadoManga.EMISION)
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    review = models.JSONField(default=list, validators=[validador_review])
    id_autor = models.UUIDField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.rating is not None and not isinstance(self.rating, Decimal):
            rating_value = str(self.rating).replace(',', '.')
            try:
                self.rating = Decimal(rating_value)
            except (InvalidOperation, ValueError, TypeError):
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Autor(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    nombre = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    def __str__(self):
        return self.nombre
