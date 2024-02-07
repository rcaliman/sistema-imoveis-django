from django.contrib import admin
from .models import EnergiaLabels


@admin.register(EnergiaLabels)
class AdminEnergiaDescricao(admin.ModelAdmin): ...
