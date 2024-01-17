from django.urls import path
from apps.imoveis.views.contrato import contrato_form, contrato

urlpatterns = [
    path('contrato_form/<int:registro_id>', contrato_form, name='contrato_form'),
    path('contrato/', contrato, name='contrato'),
]
