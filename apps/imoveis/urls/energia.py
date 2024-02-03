from django.urls import path
from ..views.energia import energia_lista, energia_inserir, energia_editar

urlpatterns = [
    path("lista/", energia_lista, name="energia_lista"),
    path("inserir/", energia_inserir, name="energia_inserir"),
    path("editar/<int:energia_id>", energia_editar, name="energia_editar"),
]
