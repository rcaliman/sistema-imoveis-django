from django.db import models


class Energia(models.Model):
    data = models.DateField(
        verbose_name="data de leitura",
        blank=False,
        null=False,
    )
    relogio_1 = models.IntegerField(
        verbose_name="valor do relógio 1",
        null=False,
        blank=False,
    )
    relogio_2 = models.IntegerField(
        verbose_name="valor do relógio 2",
        null=False,
        blank=False,
    )
    relogio_3 = models.IntegerField(
        verbose_name="valor do relógio 3",
        null=False,
        blank=False,
    )
    valor_kwh = models.FloatField(
        verbose_name="valor do kWh",
        null=True,
        blank=True,
    )
    valor_conta = models.FloatField(
        verbose_name="valor da conta",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.data
