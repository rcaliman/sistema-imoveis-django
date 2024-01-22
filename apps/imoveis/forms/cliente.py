from django import forms
from apps.imoveis.models import Cliente
import helper
from django.core.exceptions import ValidationError


class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "nome",
            "data_nascimento",
            "ci",
            "cpf",
            "telefone_1",
            "telefone_2",
            "nacionalidade",
            "estado_civil",
            "cidade_residencia_sede",
        ]
        labels = {
            "cidade_residencia_sede": "Residência/Sede",
            "cpf": "CPF/CNPJ",
        }
        tipo_choices = [
            ("pessoa física", "pessoa física"),
            ("pesoa jurídica", "pessoa jurídica"),
        ]
        labels = {
            "data_nascimento": "Data de nascimento",
            "ci": "Documento de identidade",
            "cpf": "CPF/CNPJ",
            "telefone_1": "Telefone",
            "telefone_2": "Telefone",
            "cidade_residencia_sede": "Residência/Sede",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_1": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_2": forms.TextInput(attrs={"class": "form-control"}),
            "nacionalidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado_civil": forms.TextInput(attrs={"class": "form-control"}),
            "cidade_residencia_sede": forms.TextInput(attrs={"class": "form-control"}),
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

    def clean_telefone_1(self):
        telefone_1 = self.cleaned_data["telefone_1"]
        if telefone_1 != None:
            return helper.formata_telefone(telefone_1)
        return telefone_1

    def clean_telefone_2(self):
        telefone_2 = self.cleaned_data["telefone_2"]
        if telefone_2 != None:
            return helper.formata_telefone(telefone_2)
        return telefone_2
