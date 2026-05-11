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
    # 1. Usamos el nombre exacto del modelo ('genres') pero como texto
    genres = forms.CharField(
        label="Géneros * (separados por coma)",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Shonen, Acción, Comedia'})
    )

    class Meta:
        model = Anime
        # 2. Ahora SÍ incluimos 'genres' en los fields
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

    # 3. Este método especial de Django intercepta el texto ANTES de mandarlo al modelo
    def clean_genres(self):
        genres_raw = self.cleaned_data.get('genres', '')
        
        # Convertimos el texto separado por comas a una lista
        genres_list = [g.strip() for g in genres_raw.split(',') if g.strip()]
        
        # Si la lista quedó vacía (ej: el usuario solo puso comas), lanzamos error
        if len(genres_list) == 0:
            raise ValidationError("Debe ingresar al menos un género válido.")
            
        # Lo que retornamos aquí, Django se lo inyecta automáticamente al modelo como lista
        return genres_list