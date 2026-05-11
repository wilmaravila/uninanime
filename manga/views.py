import uuid

from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Manga
from .forms import AutorForm, MangaForm, ReviewForm


# Create your views here.

def manga_list(request):
    mangas = Manga.objects.all()
    return render(request, "manga/list_manga.html", {"mangas": mangas})

def manga_detail(request, pk):
    manga = get_object_or_404(Manga, pk=pk)

    return render(request, "manga/description_manga.html", {
        "manga": manga
    })

def manga_create(request):
    if request.method == 'POST':
        form = MangaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manga_list')
    else:
        form = MangaForm()

    return render(request, 'manga/form_manga.html', {'form': form})


def manga_update(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    
    if request.method == 'POST':
        form = MangaForm(request.POST, instance=manga)
        if form.is_valid():
            form.save()
            return redirect('manga_detail', pk=manga.id)
    else:
        form = MangaForm(instance=manga)

    return render(request, 'manga/form_manga.html', {
        'form': form,
        'editing': True
    })


def autor_create(request):
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manga_create')
    else:
        form = AutorForm()

    return render(request, 'manga/add_autor.html', {
        'form': form
    })


def manga_delete(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    manga.delete()
    return redirect('manga_list')


def manga_add_review(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            nueva_review = {
                "user_id": str(uuid.uuid4()),
                "username": form.cleaned_data['username'],
                "rating": form.cleaned_data['rating'],
                "comment": form.cleaned_data['comment'],
            }

            if not isinstance(manga.review, list):
                manga.review = []

            manga.review.append(nueva_review)
        
            manga.save()
            return redirect('manga_detail', pk=manga.id)
          
    else:
        form = ReviewForm()

    return render(request, 'manga/add_review.html', {
        'form': form,
        'manga': manga
    })
def manga_delete_review(request, manga_pk, review_index):
    manga = get_object_or_404(Manga, pk=manga_pk)
    
    if 0 <= review_index < len(manga.review):
        del manga.review[review_index]
        manga.save()
    
    return redirect('manga_detail', pk=manga.id)
def manga_update_review(request, manga_pk, review_index):
    manga = get_object_or_404(Manga, pk=manga_pk)
    
    if not isinstance(manga.review, list):
        manga.review = []

    if 0 <= review_index < len(manga.review):
        review_data = manga.review[review_index]
        
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review_data['username'] = form.cleaned_data['username']
                review_data['rating'] = float(form.cleaned_data['rating'])
                review_data['comment'] = form.cleaned_data['comment']
                try:
                    manga.save()
                    return redirect('manga_detail', pk=manga.id)
                except Exception as e:
                    form.add_error(None, f"No se pudo actualizar la reseña: {e}")
        else:
            form = ReviewForm(initial={
                'username': review_data.get('username', ''),
                'rating': review_data.get('rating', 0),
                'comment': review_data.get('comment', '')
            })

        return render(request, 'manga/update_review.html', {
            'form': form,
            'manga': manga,
            'review_index': review_index
        })
    else:
        return redirect('manga_detail', pk=manga.id)
def manga_list_by_autor(request, autor_id):
    mangas = Manga.objects.filter(id_autor=autor_id)
    return render(request, "manga/list_manga.html", {"mangas": mangas})

def all_reviews(request, pk):
    manga = get_object_or_404(Manga, pk=pk)
    return render(request, "manga/all_reviews.html", {
        "manga": manga,
        "reviews": manga.review
    })