# Generated by Django 4.2.1 on 2024-02-05 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0007_energiadescricao'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EnergiaDescricao',
            new_name='EnergiaLabels',
        ),
    ]
