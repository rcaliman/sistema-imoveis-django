from django.urls import path
from apps.imoveis.views.contrato import contrato_form, contrato, contrato_imprimir, contratos_listar

urlpatterns = [
    path('contrato_form/<int:registro_id>', contrato_form, name='contrato_form'),
    path('contrato_imprimir/', contrato_imprimir, name='contrato_imprimir'),
    path('contratos_listar/', contratos_listar, name='contratos_listar'),
    path('contrato/', contrato, name='contrato'),
]
