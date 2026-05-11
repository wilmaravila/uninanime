from django.urls import path
from . import views

urlpatterns = [
    path('',             views.lista,             name='com_lista'),
    path('nueva/',       views.nueva_publicacion, name='com_nueva'),
    path('<int:pk>/',    views.detalle,           name='com_detalle'),
    path('sugerencias/', views.sugerencias,       name='com_sugerencias'),
]