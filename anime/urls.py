from django.urls import path
from .views import *

urlpatterns = [
    path("", anime_list, name="anime_list"),
    path("anime/<int:pk>/", anime_detail, name="anime_detail"),
    path('anime/add/', anime_create, name='anime_create'),
    path('anime/edit/<int:pk>/', anime_update, name='anime_update'),
    path('anime/<int:pk>/review/add/', add_review, name='add_review'),
    path('anime/<int:pk>/review/delete/<str:username>/', delete_review, name='delete_review'),
    path('anime/<int:pk>/reviews/', all_reviews, name='all_reviews'),
    path('anime/delete/<int:pk>/', anime_delete, name='anime_delete'),
]