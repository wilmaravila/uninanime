from django.urls import path
from .views import anime_list, anime_detail, anime_create

urlpatterns = [
    path("", anime_list, name="anime_list"),
    path("anime/<int:pk>/", anime_detail, name="anime_detail"),
    path('anime/add/', anime_create, name='anime_create'),
]