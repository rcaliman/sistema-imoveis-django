from django.db import models
from .imovel import Imovel


class Historico(models.Model):
    data = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=100, null=False, blank=True)
    numero = models.CharField(max_length=5, null=False, blank=True)
    local = models.CharField(max_length=100, null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    complemento = models.CharField(max_length=250, null=True, blank=True)
    observacao = models.CharField(max_length=250, null=True, blank=True)
    dia = models.IntegerField(null=True, blank=True)
    cliente_nome = models.CharField(max_length=200, null=True, blank=True)
    cliente_cpf_cnpj = models.CharField(max_length=200, null=True, blank=True)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)