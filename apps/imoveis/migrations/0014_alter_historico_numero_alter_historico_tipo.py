# Generated by Django 4.2.1 on 2024-05-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0013_alter_locador_principal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='numero',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='historico',
            name='tipo',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]