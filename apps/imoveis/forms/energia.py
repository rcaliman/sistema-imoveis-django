from django import forms
from apps.imoveis.models.energia import Energia


class FormEnergia(forms.ModelForm):
    class Meta:
        model = Energia
        fields = "__all__"

        widgets = {
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "relogio_1": forms.TextInput(attrs={"class": "form-control"}),
            "relogio_2": forms.TextInput(attrs={"class": "form-control"}),
            "relogio_3": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_kwh": forms.NumberInput(attrs={"class": "form-control"}),
            "valor_conta": forms.NumberInput(attrs={"class": "form-control"}),
        }
