from django import forms
from apps.imoveis.models.locador import Locador


class FormLocador(forms.ModelForm):
    class Meta:
        model = Locador

        fields = [
            "nome",
            "cpf",
            "residencia",
            "estado_civil",
            "data_nascimento",
            "telefone",
            "email",
            "nacionalidade"
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "residencia": forms.TextInput(attrs={"class": "form-control"}),
            "estado_civil": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d",
            ),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "nacionalidade": forms.TextInput(attrs={"class": "form-control"})
        }
