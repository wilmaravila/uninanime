from django import forms
from django.core.exceptions import ValidationError
from .models import Anime

class AnimeForm(forms.ModelForm):

    genres = forms.CharField(help_text="Ej: fantasia, accion")

    class Meta:
        model = Anime
        fields = "__all__"

    def clean_genres(self):
        data = self.cleaned_data["genres"]
        return [g.strip() for g in data.split(",")]
    
class AnimeForm(forms.ModelForm):
    genres = forms.CharField(
        label="Géneros * (separados por coma)",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Shonen, Acción, Comedia'})
    )

    class Meta:
        model = Anime
        fields = ['title', 'poster_url', 'episodes', 'release_year', 'genres', 'synopsis']
        
        labels = {
            'title': 'Título de la serie *',
            'poster_url': 'URL del Póster',
            'episodes': 'Episodios *',
            'release_year': 'Año de emisión *',
            'synopsis': 'Sinopsis *'
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ej: Evangelion'}),
            'poster_url': forms.URLInput(attrs={'placeholder': 'https://ejemplo.com/imagen.jpg'}),
            'synopsis': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe de qué trata el anime...'}),
        }

    def __init__(self, *args, **kwargs):
        super(AnimeForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            genres_data = self.instance.genres
            
            
            if isinstance(genres_data, list):
                self.fields['genres'].initial = ", ".join(genres_data)
            
            
            elif isinstance(genres_data, str):
                limpio = genres_data.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
                self.fields['genres'].initial = limpio

    def clean_genres(self):
        genres_raw = self.cleaned_data.get('genres', '')
        genres_list = [g.strip() for g in genres_raw.split(',') if g.strip()]
        if len(genres_list) == 0:
            raise ValidationError("Debe ingresar al menos un género.")
        return genres_list
    
class ReviewForm(forms.Form):
    username = forms.CharField(
        label="Tu nombre de usuario *",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: OtakuMaster99'})
    )
    
    rating = forms.IntegerField(
        label="Calificación (1 a 5) *",
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5})
    )
    
    comment = forms.CharField(
        label="Título de la reseña *",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: ¡Obra maestra!'})
    )
    
    description = forms.CharField(
        label="Descripción completa (Opcional)",
        required=False, 
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': '¿Qué te pareció la animación, la historia...?'})
    )

class CharacterForm(forms.Form):
    name = forms.CharField(
        label="Nombre del Personaje *",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Shinji Ikari'})
    )
    
    role = forms.ChoiceField(
        label="Rol en la serie *",
        choices=[
            ('Protagonista', 'Protagonista'),
            ('Secundario', 'Secundario'),
            ('Antagonista', 'Antagonista')
        ],
        widget=forms.RadioSelect(attrs={'class': 'role-radio-group'})
    )
    
    image_url = forms.URLField(
        label="URL de la imagen",
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'https://ejemplo.com/personaje.jpg'})
    )