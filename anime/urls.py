from django.urls import path
from .views import anime_list

urlpatterns = [
    path("", anime_list, name="anime_list"),
]