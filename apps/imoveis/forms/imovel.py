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
            "iptu_inscricao",
            "iptu_titular",
            "elfsm_inscricao",
            "elfsm_titular",
        ]
        labels = {
            "dia": "Dia de pagamento",
            "observacao": "Observações",
            "iptu_inscricao": "Inscrição do IPTU",
            "iptu_titular": "Titular do IPTU",
            "elfsm_inscricao": "Inscrição conta de energia",
            "elfsm_titular": "Titular da conta de energia",
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
            "iptu_inscricao": forms.NumberInput(attrs={"class": "form-control"}),
            "iptu_titular": forms.Select(attrs={"class": "form-control"}),
            "elfsm_inscricao": forms.NumberInput(attrs={"class": "form-control"}),
            "elfsm_titular": forms.Select(attrs={"class": "form-control"}),
        }
