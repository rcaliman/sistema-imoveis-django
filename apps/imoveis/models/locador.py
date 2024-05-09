from django.db import models


class Locador(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    residencia = models.CharField(max_length=200, blank=True, null=True)
    estado_civil = models.CharField(max_length=100, blank=True, null=True)
    data_nascimento = models.DateField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    nacionalidade = models.CharField(max_length=200, blank=True, null=True)
    principal = models.BooleanField(default=False, null=None, blank=None)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]
