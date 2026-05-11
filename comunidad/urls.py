from django.urls import path
from . import views

urlpatterns = [
    path('',                   views.lista,                name='com_lista'),
    path('nueva/',             views.nueva_publicacion,    name='com_nueva'),
    path('<int:pk>/',          views.detalle,              name='com_detalle'),
    path('<int:pk>/editar/',   views.editar_publicacion,   name='com_editar'),
    path('<int:pk>/eliminar/', views.eliminar_publicacion, name='com_eliminar'),
    path('sugerencias/',       views.sugerencias,          name='com_sugerencias'),
]