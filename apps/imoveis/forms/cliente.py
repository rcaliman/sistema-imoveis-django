from django import forms
from apps.imoveis.models import Cliente


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
            "tipo",
            "nacionalidade",
            "estado_civil",
            "cidade_residencia_sede",
        ]
        labels = {
            'cidade_residencia_sede': 'Residência/Sede',
        }
        tipo_choices = [
            ('pessoa física', 'pessoa física'),
            ('pesoa jurídica', 'pessoa jurídica'),
        ]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "ci": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_1": forms.TextInput(attrs={"class": "form-control"}),
            "telefone_2": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-control"}, choices=tipo_choices),
            "nacionalidade": forms.TextInput(attrs={"class": "form-control"}),
            "estado_civil": forms.TextInput(attrs={"class": "form-control"}),
            "cidade_residencia_sede": forms.TextInput(attrs={"class": "form-control"}),
        }
