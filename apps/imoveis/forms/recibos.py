from django import forms
from calendar import month_name
from datetime import datetime
from apps.imoveis.models import Locatario
from apps.imoveis.models import Imovel

class FormRecibos(forms.Form):
    def choices_locatarios() -> list[tuple[str, str]]:
        obj = Locatario.objects.all().order_by('nome')
        locatarios = []
        for l in obj:
            locatarios.append(
                (l.nome, l.nome)
            )
        return locatarios
    
    def choices_meses() -> list[tuple[str, str]]:
        meses = []
        for i in range(1, 13):
            meses.append((month_name[i], month_name[i]))
        return meses
    
    def mes_atual() -> tuple[str, str]:
        mes_atual = (month_name[datetime.now().month], month_name[datetime.now().month])
        return mes_atual
    
    def choices_anos() -> list[tuple[str, str]]:
        ano_atual = datetime.now().year
        anos = [
            (
                str(ano_atual - 1), str(ano_atual - 1)
            ),
            (
                str(ano_atual), str(ano_atual)
            ),
            (
                str(ano_atual + 1), str(ano_atual + 1)
            ),
        ]
        return anos

    def ano_atual() -> tuple[str, str]:
        ano_atual = (str(datetime.now().year), str(datetime.now().year))
        return ano_atual
    
    def codigos_imoveis() -> list[tuple[int,str]]:
        lista = Imovel.objects.all().values_list(flat=True)
        codigos = []
        for i in lista:
            codigos.append((i,''))
        return codigos
    
    select_locatario = forms.ChoiceField(
        choices=choices_locatarios,
        widget=forms.Select(
            attrs={
                'class': 'inputgerarrecibo',
                'id': 'recibo_locatario',
            }
        )
    )
    
    select_mes = forms.ChoiceField(
        initial=mes_atual,
        choices=choices_meses,
        widget=forms.Select(
            attrs={
                'name': 'recibo_mes',
                'class': 'inputgerarrecibo',
                'id': 'recibo_mes',
            }
        )
    )
    select_ano = forms.ChoiceField(
        initial=ano_atual,
        choices=choices_anos,
        widget=forms.Select(
            attrs={
                'name': 'recibo_ano',
                'class': 'inputgerarrecibo',
                'id': 'recibo_ano',
            }
        )
    )
