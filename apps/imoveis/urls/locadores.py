from django.urls import path
from ..views.locador import (
    locadores_lista,
    locador_inserir,
    locador_apagar,
    locador_alterar,
)

urlpatterns = [
    path("lista/", locadores_lista, name="locadores_lista"),
    path("inserir/", locador_inserir, name="locador_inserir"),
    path("apagar/<int:id_do_registro>", locador_apagar, name="locador_apagar"),
    path("alterar/<int:id_do_registro>", locador_alterar, name="locador_alterar"),
]
