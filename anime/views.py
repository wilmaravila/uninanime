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
            return redirect('anime_list') 
            
    else:
        form = AnimeForm(initial={'episodes': 1, 'release_year': 2024})

    return render(request, 'anime/new_anime.html', {'form': form})

def anime_update(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    
    if request.method == 'POST':
        form = AnimeForm(request.POST, instance=anime)
        if form.is_valid():
            form.save()
            return redirect('anime_detail', pk=anime.id) 
    else:
        # Al cargar por primera vez, pasamos el anime actual al formulario
        form = AnimeForm(instance=anime)
    
    return render(request, 'anime/form_anime.html', {
        'form': form,
        'editing': True
    })