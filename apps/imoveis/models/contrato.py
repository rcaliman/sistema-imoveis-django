from django.db import models
from ..models.imovel import Imovel

class Contrato(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data_impressao = models.DateField(auto_now_add=True)
    texto = models.TextField(blank=True, null=True)