from django import forms
from apps.imoveis.models.locador import Locador
from django.core.exceptions import ValidationError
import helper


class FormLocador(forms.ModelForm):
    class Meta:
        model = Locador

        select_principal = [
            (True, 'Sim'),
            (False, 'Não'),
        ]

        fields = [
            "nome",
            "cpf",
            "residencia",
            "estado_civil",
            "data_nascimento",
            "telefone",
            "email",
            "nacionalidade",
            "principal",
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
            "nacionalidade": forms.TextInput(attrs={"class": "form-control"}),
            "principal": forms.Select(choices=select_principal, attrs={"class": "form-control"}),
        }
    
    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        if cpf != None:
            cpf_verificado = helper.verifica_documento(cpf)
            if cpf_verificado.get("documento"):
                return cpf_verificado["numero_formatado"]
            else:
                raise ValidationError("Número inválido")
        return cpf
