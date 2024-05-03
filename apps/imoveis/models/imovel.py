from django.db import models
from ..models.cliente import Cliente
from ..models.locador import Locador


class Imovel(models.Model):
    tipo = models.CharField(max_length=100, null=False)
    numero = models.CharField(max_length=5, null=False)
    local = models.CharField(max_length=100, null=True, blank=True)
    cliente = models.ForeignKey(
        Cliente, null=True, blank=True, on_delete=models.SET_NULL
    )
    valor = models.FloatField(null=True, blank=True)
    complemento = models.CharField(max_length=250, null=True, blank=True)
    observacao = models.CharField(max_length=250, null=True, blank=True)
    dia = models.IntegerField(null=True, blank=True)
    iptu_inscricao = models.IntegerField(null=True, blank=True)
    iptu_titular = models.ForeignKey(Locador, null=True, blank=True, on_delete=models.SET_NULL, related_name='iptu_titular')
    elfsm_inscricao = models.IntegerField(null=True, blank=True)
    elfsm_titular = models.ForeignKey(Locador, null=True, blank=True, on_delete=models.SET_NULL, related_name='elfsm_titular')

    class Meta:
        ordering = ["cliente"]
