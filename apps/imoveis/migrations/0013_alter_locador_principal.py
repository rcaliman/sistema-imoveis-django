# Generated by Django 4.2.1 on 2024-05-09 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0012_alter_locador_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locador',
            name='principal',
            field=models.BooleanField(blank=None, default=False, null=None),
        ),
    ]