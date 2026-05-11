from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',     admin.site.urls),
    path('',           include('comunidad.urls')),
    path('comunidad/', include('comunidad.urls')),
    path('animes/',     include('anime.urls')),
    path('manga/',     include('manga.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)