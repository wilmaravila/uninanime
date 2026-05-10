from django.shortcuts import render
from .models import Anime

def anime_list(request):
    animes = Anime.objects.all()
    return render(request, "anime/list.html", {"animes": animes})