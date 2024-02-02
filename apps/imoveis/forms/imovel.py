from django import forms
from apps.imoveis.models.imovel import Imovel


class FormImovel(forms.ModelForm):
    class Meta:
        CHOICES_TIPO = [
            ("apartamento", "apartamento"),
            ("sala comercial", "sala comercial"),
            ("loja", "loja"),
            ("kitnet", "kitnet"),
            ("condomínio", "condomínio"),
            ("", ""),
        ]
        model = Imovel
        fields = [
            "tipo",
            "numero",
            "local",
            "cliente",
            "valor",
            "complemento",
            "observacao",
            "dia",
        ]
        labels = {
            "dia": 'Dia de pagamento',
            "observacao": "Observações",
        }
        widgets = {
            "tipo": forms.Select(
                attrs={"class": "form-control"}, choices=sorted(CHOICES_TIPO)
            ),
            "numero": forms.TextInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control"}),
            "complemento": forms.TextInput(attrs={"class": "form-control"}),
            "observacao": forms.TextInput(attrs={"class": "form-control"}),
            "dia": forms.NumberInput(attrs={"class": "form-control"}),
        }
