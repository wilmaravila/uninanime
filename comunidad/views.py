from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Publicacion
from .forms  import PublicacionForm, SugerenciaForm


def lista(request):
    tipo  = request.GET.get('tipo', '')
    todas = list(Publicacion.objects.all())

    # Filtramos en Python por el bug de Djongo con BooleanFields
    todas = [p for p in todas if p.publicada]

    if tipo:
        todas = [p for p in todas if p.tipo == tipo]

    destacadas = [p for p in todas if p.destacada]
    hero       = destacadas[0] if destacadas else None
    aside      = destacadas[1:4]
    grid       = [p for p in todas if not p.destacada]

    return render(request, 'comunidad/lista.html', {
        'hero':  hero,
        'aside': aside,
        'grid':  grid,
        'tipos': Publicacion.TIPOS,
        'tipo':  tipo,
    })


def detalle(request, pk):
    pub          = get_object_or_404(Publicacion, pk=pk)
    todas        = list(Publicacion.objects.all())
    relacionadas = [p for p in todas if p.tipo == pub.tipo and p.pk != pub.pk][:4]

    return render(request, 'comunidad/detalle.html', {
        'pub':          pub,
        'relacionadas': relacionadas,
        'etiquetas':    pub.get_etiquetas_lista(),
    })


def nueva_publicacion(request):
    """
    GET  → muestra el formulario vacío.
    POST → valida, guarda en MongoDB y redirige a la lista.
    """
    if request.method == 'POST':
        # request.FILES es necesario para recibir la imagen de portada
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion          = form.save(commit=False)
            publicacion.publicada = True
            publicacion.save()
            messages.success(request, f'✅ "{publicacion.titulo}" publicado correctamente.')
            return redirect('com_lista')
    else:
        form = PublicacionForm()

    return render(request, 'comunidad/nueva.html', {'form': form})


def sugerencias(request):
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                f'¡Gracias {form.cleaned_data["nombre"]}! Recibimos tu sugerencia.'
            )
            return redirect('com_lista')
    else:
        form = SugerenciaForm()

    return render(request, 'comunidad/sugerencias.html', {'form': form})