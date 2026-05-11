from django.shortcuts import redirect, render, get_object_or_404
from .models import Anime
from .forms import AnimeForm

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

def anime_create(request):
    if request.method == 'POST':
        form = AnimeForm(request.POST)
        
        if form.is_valid():
            form.save()
            # Asegúrate de que 'anime_list' sea el nombre de la URL de tu lista
            return redirect('anime_list') 
            
    else:
        form = AnimeForm(initial={'episodes': 1, 'release_year': 2024})

    return render(request, 'anime/new_anime.html', {'form': form})