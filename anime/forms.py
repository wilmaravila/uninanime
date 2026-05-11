from django import forms
from .models import Anime

class AnimeForm(forms.ModelForm):

    genres = forms.CharField(help_text="Ej: fantasia, accion")

    class Meta:
        model = Anime
        fields = "__all__"

    def clean_genres(self):
        data = self.cleaned_data["genres"]
        return [g.strip() for g in data.split(",")]