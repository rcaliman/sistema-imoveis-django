from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=False)
    data_nascimento = models.DateField(null=True, blank=True)
    ci = models.CharField(max_length=200, null=True, blank=True)
    cpf = models.CharField(max_length=200, null=True, blank=True)
    telefone_1 = models.CharField(max_length=100, null=True, blank=True)
    telefone_2 = models.CharField(max_length=100, null=True, blank=True)
    nacionalidade = models.CharField(max_length=200, null=True, blank=True)
    estado_civil = models.CharField(max_length=200, null=True, blank=True)
    cidade_residencia_sede = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]
