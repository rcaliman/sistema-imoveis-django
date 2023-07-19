from django.db import models


class Locatario(models.Model):
    nome = models.TextField(max_length=200, blank=False, null=False)
    cpf = models.TextField(max_length=20, blank=True, null=False)
    residencia = models.TextField(max_length=200, blank=True, null=False)
    estado_civil = models.TextField(max_length=100, blank=True, null=False)
    data_nascimento = models.DateField(max_length=100, blank=True, null=False)
    telefone = models.TextField(max_length=100, blank=True, null=False)
    email = models.TextField(max_length=200, blank=True, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]
