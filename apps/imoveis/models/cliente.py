from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=200, null=False)
    data_nascimento = models.DateField(null=False, blank=True)
    ci = models.CharField(max_length=200, null=False, blank=True)
    cpf = models.CharField(max_length=200, null=False, blank=True)
    telefone_1 = models.CharField(max_length=100, null=False, blank=True)
    telefone_2 = models.CharField(max_length=100, null=False, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]
