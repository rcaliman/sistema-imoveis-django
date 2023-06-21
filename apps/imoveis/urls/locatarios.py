from django.urls import path
from apps.imoveis.views.locatario import (
    locatarios_lista,
    locatario_inserir,
    locatario_apagar,
    locatario_alterar,
)

urlpatterns = [
    path("lista/", locatarios_lista, name="locatarios_lista"),
    path("inserir/", locatario_inserir, name="locatario_inserir"),
    path("apagar/<int:id_do_registro>", locatario_apagar, name="locatario_apagar"),
    path("alterar/<int:id_do_registro>", locatario_alterar, name="locatario_alterar"),
]
