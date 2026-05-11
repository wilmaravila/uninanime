from decimal import Decimal, InvalidOperation

from django import forms
from django.core.exceptions import ValidationError

from .models import Autor, Manga


class MangaForm(forms.ModelForm):

    generos = forms.CharField(
        label="Géneros *",
        required=True,
        help_text="Separados por coma",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Acción, Shonen, Fantasía'
            }
        )
    )

    autor = forms.ModelChoiceField(
        queryset=Autor.objects.all(),
        required=False,
        label='Autor',
        empty_label='Seleccionar autor existente'
    )

    class Meta:
        model = Manga

        fields = [
            'titulo',
            'descripcion',
            'poster_url',
            'generos',
            'capitulos',
            'estado',
            'rating'
        ]

        labels = {
            'titulo': 'Título del manga *',
            'descripcion': 'Descripción *',
            'poster_url': 'URL de la portada',
            'capitulos': 'Cantidad de capítulos *',
            'estado': 'Estado del manga *',
            'rating': 'Rating *',
            'id_autor': 'ID del autor'
        }

        widgets = {

            'titulo': forms.TextInput(
                attrs={
                    'placeholder': 'Ej: Berserk'
                }
            ),

            'descripcion': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Describe el manga...'
                }
            ),

            'poster_url': forms.URLInput(
                attrs={
                    'placeholder': 'https://ejemplo.com/imagen.jpg'
                }
            ),

            'capitulos': forms.NumberInput(
                attrs={
                    'min': 1
                }
            ),

          
        }

    def __init__(self, *args, **kwargs):

        super(MangaForm, self).__init__(*args, **kwargs)

        # Convertir lista → string
        if self.instance and self.instance.pk:

            generos_data = self.instance.generos

            if isinstance(generos_data, list):

                self.fields['generos'].initial = ", ".join(generos_data)

            if self.instance.id_autor:
                try:
                    self.fields['autor'].initial = Autor.objects.get(id=self.instance.id_autor)
                except Autor.DoesNotExist:
                    self.fields['autor'].initial = None

    def save(self, commit=True):
        instance = super(MangaForm, self).save(commit=False)
        autor = self.cleaned_data.get('autor')
        instance.id_autor = autor.id if autor else None
        if commit:
            instance.save()
        return instance

    def clean_generos(self):

        generos_raw = self.cleaned_data.get('generos', '')

        generos_list = [
            g.strip()
            for g in generos_raw.split(',')
            if g.strip()
        ]

        if len(generos_list) == 0:

            raise ValidationError(
                "Debe ingresar al menos un género."
            )

        return generos_list


class AutorForm(forms.ModelForm):

    class Meta:
        model = Autor
        fields = [
            'nombre',
            'fecha_nacimiento'
        ]
        labels = {
            'nombre': 'Nombre del autor *',
            'fecha_nacimiento': 'Fecha de nacimiento *'
        }
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ej: Kentaro Miura'
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            )
        }
class ReviewForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario *",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ej: AnimeFan123'
            }
        )
    )
    rating = forms.IntegerField(
        label="Calificación *",
        widget=forms.NumberInput(
            attrs={
                
                'min': '0',
                'max': '5',
                
            }
        )
    )
    comment = forms.CharField(
        label="Comentario *",
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'placeholder': 'Escribe tu comentario sobre el manga...'
            }
        )
    )

 