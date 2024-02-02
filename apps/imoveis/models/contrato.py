from django.db import models
from apps.imoveis.models.imovel import Imovel

class Contrato(models.Model):
    imovel = models.ForeignKey(to=Imovel, on_delete=models.CASCADE)
    data_impressao = models.DateField(auto_now_add=True)
    texto = models.TextField(blank=True, null=True)