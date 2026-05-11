from django.contrib import admin
from .models import Anime
from .forms import AnimeForm

class AnimeAdmin(admin.ModelAdmin):
    form = AnimeForm

admin.site.register(Anime, AnimeAdmin)