from django.db import models


class Publicacion(models.Model):

    TIPOS = [
        ('noticia',       'Noticia'),
        ('estreno',       'Estreno'),
        ('resena',        'Reseña'),
        ('recomendacion', 'Recomendación'),
        ('lista',         'Lista / Top'),
        ('entrevista',    'Entrevista'),
    ]

    PUNTUACIONES = [(i, str(i)) for i in range(1, 11)]

    tipo          = models.CharField(max_length=20, choices=TIPOS, default='noticia')
    titulo        = models.CharField(max_length=500)
    resumen       = models.CharField(max_length=300)
    contenido     = models.TextField()
    autor         = models.CharField(max_length=100)
    portada       = models.ImageField(upload_to='comunidad/', blank=True, null=True)
    etiquetas     = models.CharField(max_length=300, blank=True)
    puntuacion    = models.IntegerField(choices=PUNTUACIONES, null=True, blank=True)
    fecha_estreno = models.DateField(null=True, blank=True)
    anime_nombre  = models.CharField(max_length=200, blank=True)
    manga_nombre  = models.CharField(max_length=200, blank=True)
    destacada     = models.BooleanField(default=False)
    publicada     = models.BooleanField(default=True)
    creado        = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Publicaciones'
        ordering            = ['-creado']

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.titulo}"

    def get_etiquetas_lista(self):
        return [e.strip() for e in self.etiquetas.split(',')] if self.etiquetas else []