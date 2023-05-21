from django.urls import path
from imoveis.views.clientes import clientes_lista, cliente_inserir, cliente_alterar, cliente_apagar

urlpatterns = [
    path('lista/', clientes_lista, name='clientes_lista'),
    path('inserir/', cliente_inserir, name='cliente_inserir'),
    path('alterar/<int:id_do_registro>', cliente_alterar, name='cliente_alterar'),
    path('apagar/<int:id_do_registro>', cliente_apagar, name='cliente_apagar'),
]
