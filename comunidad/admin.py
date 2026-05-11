from django.contrib import admin
from .models import Publicacion


@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):

    list_display  = ['titulo', 'tipo', 'autor', 'puntuacion', 'destacada', 'publicada', 'creado']
    list_filter   = ['tipo', 'destacada', 'publicada']
    list_editable = ['destacada', 'publicada']
    search_fields = ['titulo', 'autor', 'etiquetas']
    readonly_fields = ['creado']

    fieldsets = [
        ('Principal',   {'fields': ['tipo', 'titulo', 'resumen', 'contenido', 'autor', 'portada']}),
        ('Relacionado', {'fields': ['anime_nombre', 'manga_nombre']}),
        ('Extras',      {'fields': ['etiquetas', 'puntuacion', 'fecha_estreno']}),
        ('Visibilidad', {'fields': ['destacada', 'publicada', 'creado']}),
    ]