from django.shortcuts import render, get_object_or_404
from .models import Anime

def anime_list(request):
    animes = Anime.objects.all()
    for anime in animes:
        print(anime)

    return render(request, "anime/list.html", {"animes": animes})

def anime_detail(request, pk):
    anime = get_object_or_404(Anime, pk=pk)

    return render(request, "anime/description_anime.html", {
        "anime": anime
    })