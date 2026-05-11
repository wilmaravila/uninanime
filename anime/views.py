from django.shortcuts import redirect, render, get_object_or_404
from .models import Anime
from django.core.exceptions import ValidationError
from .forms import AnimeForm, ReviewForm

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

    return render(request, 'anime/form_anime.html', {'form': form})

def anime_update(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    
    if request.method == 'POST':
        form = AnimeForm(request.POST, instance=anime)
        if form.is_valid():
            form.save()
            return redirect('anime_detail', pk=anime.id) 
    else:
        form = AnimeForm(instance=anime)
    
    return render(request, 'anime/form_anime.html', {
        'form': form,
        'editing': True
    })

def anime_delete(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    anime.delete()
    return redirect('anime_list')

def add_review(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            nueva_review = {
                "username": form.cleaned_data['username'],
                "rating": form.cleaned_data['rating'],
                "comment": form.cleaned_data['comment'],
                "description": form.cleaned_data['description'] or "Sin descripción"
            }
            
            anime.reviews.append(nueva_review)
            
            try:
                anime.save() 
                return redirect('anime_detail', pk=anime.id)
            except ValidationError as e:
                error_msg = e.messages[0] if hasattr(e, 'messages') else str(e)
                form.add_error(None, error_msg)
    else:
        form = ReviewForm()

    return render(request, 'anime/add_review.html', {
        'form': form,
        'anime': anime
    })

def delete_review(request, pk, username):
    anime = get_object_or_404(Anime, pk=pk)
    
    anime.reviews = [r for r in anime.reviews if r.get('username') != username]
    
    anime.save() 
    return redirect('anime_detail', pk=pk)

def all_reviews(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    
    reviews = reversed(anime.reviews) 
    return render(request, 'anime/all_reviews.html', {
        'anime': anime,
        'reviews': reviews
    })