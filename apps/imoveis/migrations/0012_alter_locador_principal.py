# Generated by Django 4.2.1 on 2024-05-08 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0011_alter_locador_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locador',
            name='principal',
            field=models.BooleanField(default=False),
        ),
    ]