from django import forms
from apps.imoveis.models import Locatario


class FormLocatario(forms.ModelForm):
    class Meta:
        model = Locatario

        fields = [
            "nome",
            "cpf",
            "residencia",
            "estado_civil",
            "data_nascimento",
            "telefone",
            "email",
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "residencia": forms.TextInput(attrs={"class": "form-control"}),
            "estado_civil": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
