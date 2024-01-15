from django.urls import path
from apps.imoveis.views import imoveis_lista, imoveis_ordenados, imoveis_recibos
from apps.imoveis.views import imovel_inserir, imovel_alterar, imovel_apagar

urlpatterns = [
    path('lista/', imoveis_lista, name='imoveis_lista'),
    path('lista/<str:ordenador>', imoveis_ordenados, name='imoveis_ordenados'),
    path('inserir/', imovel_inserir, name='imovel_inserir'),
    path('editar/<int:id_do_registro>', imovel_alterar, name='imovel_alterar'),
    path('apagar/<int:id_do_registro>', imovel_apagar, name='imovel_apagar'),
    path('recibos/', imoveis_recibos, name='imoveis_recibos'),
]
