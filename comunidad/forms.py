from django import forms
from .models import Publicacion


class PublicacionForm(forms.ModelForm):

    class Meta:
        model  = Publicacion
        fields = [
            'tipo', 'titulo', 'resumen', 'contenido',
            'autor', 'portada', 'etiquetas',
            'puntuacion', 'fecha_estreno',
            'anime_nombre', 'manga_nombre',
        ]

        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-select',
                'style': 'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
                'id':    'id_tipo',
            }),
            'titulo': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Título de la publicación',
                'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
            }),
            'resumen': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Resumen corto (aparece en el grid)',
                'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
            }),
            'contenido': forms.Textarea(attrs={
                'class':       'form-control',
                'placeholder': 'Escribe el contenido completo aquí...',
                'rows':        8,
                'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
            }),
            'autor': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Tu nombre o alias',
                'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
            }),
            'etiquetas': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'demon-slayer,mappa,2025',
                'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
            }),
            'puntuacion': forms.Select(attrs={
                'class': 'form-select',
                'style': 'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
                'id':    'id_puntuacion',
            }),
            'fecha_estreno': forms.DateInput(attrs={
                'class': 'form-control',
                'type':  'date',
                'style': 'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
                'id':    'id_fecha_estreno',
            }),
            'anime_nombre': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Nombre del anime relacionado',
                'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
            }),
            'manga_nombre': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Nombre del manga relacionado',
                'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
            }),
        }

        labels = {
            'tipo':         'Tipo de publicación',
            'titulo':       'Título',
            'resumen':      'Resumen corto',
            'contenido':    'Contenido',
            'autor':        'Autor',
            'portada':      'Imagen de portada (opcional)',
            'etiquetas':    'Etiquetas (separadas por coma)',
            'puntuacion':   'Puntuación',
            'fecha_estreno':'Fecha de estreno',
            'anime_nombre': 'Anime relacionado (opcional)',
            'manga_nombre': 'Manga relacionado (opcional)',
        }

    def clean(self):
        cleaned = super().clean()
        tipo      = cleaned.get('tipo')
        puntuacion = cleaned.get('puntuacion')
        fecha      = cleaned.get('fecha_estreno')

        # Si es reseña, la puntuación es obligatoria
        if tipo == 'resena' and not puntuacion:
            self.add_error('puntuacion', 'Las reseñas requieren una puntuación.')

        # Si es estreno, la fecha es obligatoria
        if tipo == 'estreno' and not fecha:
            self.add_error('fecha_estreno', 'Los estrenos requieren una fecha.')

        return cleaned


class SugerenciaForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':       'form-control',
            'placeholder': 'Tu nombre o alias',
            'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':       'form-control',
            'placeholder': 'tucorreo@ejemplo.com',
            'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
        })
    )
    tema = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={
            'class':       'form-control',
            'placeholder': '¿Sobre qué quieres que escribamos?',
            'style':       'background:#1a1a2a;color:#e8e8f0;border:1px solid #2a2a4a;',
        })
    )

    def clean_tema(self):
        tema = self.cleaned_data['tema']
        if len(tema) < 10:
            raise forms.ValidationError('El tema debe tener al menos 10 caracteres.')
        return tema