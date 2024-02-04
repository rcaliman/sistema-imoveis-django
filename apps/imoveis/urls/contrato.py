from django.urls import path
from ..views.contrato import contrato_form, contrato, contrato_imprimir

urlpatterns = [
    path('contrato_form/<int:registro_id>', contrato_form, name='contrato_form'),
    path('contrato_imprimir/<int:registro_id>', contrato_imprimir, name='contrato_imprimir'),
    path('contrato/<int:registro_id>', contrato, name='contrato'),
]
