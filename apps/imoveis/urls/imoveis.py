from django.urls import path
from ..views.imovel import imoveis_lista, imoveis_ordenados, imoveis_recibos
from ..views.imovel import imovel_inserir, imovel_alterar, imovel_apagar, historico_listar

urlpatterns = [
    path('lista/', imoveis_lista, name='imoveis_lista'),
    path('lista/<str:ordenador>', imoveis_ordenados, name='imoveis_ordenados'),
    path('inserir/', imovel_inserir, name='imovel_inserir'),
    path('editar/<int:id_do_registro>', imovel_alterar, name='imovel_alterar'),
    path('apagar/<int:id_do_registro>', imovel_apagar, name='imovel_apagar'),
    path('recibos/', imoveis_recibos, name='imoveis_recibos'),
    path('historico_listar/<int:imovel_id>', historico_listar, name='historico_listar'),

]
