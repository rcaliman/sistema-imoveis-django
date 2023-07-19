from django.db import models
from apps.imoveis.models.cliente import Cliente


class Imovel(models.Model):
    tipo = models.CharField(max_length=100, null=False)
    numero = models.CharField(max_length=5, null=False)
    local = models.CharField(max_length=100, null=False, blank=True)
    cliente = models.ForeignKey(
        Cliente, null=True, blank=True, on_delete=models.SET_NULL
    )
    valor = models.FloatField(null=False, blank=True)
    complemento = models.CharField(max_length=250, null=False, blank=True)
    observacao = models.CharField(max_length=250, null=False, blank=True)
    dia = models.IntegerField(null=False, blank=True)

    class Meta:
        ordering = ["cliente"]
