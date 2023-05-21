from django import forms
from imoveis.models import Cliente


class FormCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome',
            'data_nascimento',
            'ci',
            'cpf',
            'telefone_1',
            'telefone_2',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_1': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone_2': forms.TextInput(attrs={'class': 'form-control'}),
        }
