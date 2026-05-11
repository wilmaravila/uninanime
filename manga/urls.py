from django.urls import path

from .views import *

urlpatterns = [
    path("", manga_list, name="manga_list"),
    path("manga/<uuid:pk>/", manga_detail, name="manga_detail"),
    path('manga/add/', manga_create, name='manga_create'),
    path('manga/edit/<uuid:pk>/', manga_update, name='manga_update'),
    path('manga/<uuid:pk>/review/add/', manga_add_review, name='manga_add_review'),
    path('manga/<uuid:manga_pk>/review/delete/<int:review_index>/', manga_delete_review, name='manga_delete_review'),
    path('manga/<uuid:manga_pk>/review/edit/<int:review_index>/', manga_update_review, name='manga_update_review'),
    path('manga/<uuid:pk>/reviews/', all_reviews, name='manga_all_reviews'),
    path('autor/add/', autor_create, name='autor_create'),
    path('autor/<uuid:autor_id>/', manga_list_by_autor, name='manga_list_by_autor'),
    path('manga/delete/<uuid:pk>/', manga_delete, name='manga_delete'),
]
