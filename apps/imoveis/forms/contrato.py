from django import forms
from apps.imoveis.models import Locador
from datetime import datetime

class FormContrato(forms.Form):
    def choices_locadores() -> list[tuple[str, str]]:
        obj = Locador.objects.all().order_by('nome')
        locadores = []
        for l in obj:
            locadores.append(
                (l.id, l.nome)
            )
        return locadores
    
    select_locador = forms.ChoiceField(
        choices=choices_locadores,
        required=False,
        label='Selecione o locador',
        widget=forms.Select(
            attrs={
                'class': 'form-control input-gerar-contrato',
                'id': 'recibo_locador',
            }
        )
    )
    choices_uso_imovel = [
        ('residencial', 'residencial'),
        ('comercial', 'comercial'),
    ]
    choices_mes = [
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]
    
    def choices_ano() -> list[tuple[str, str]]:
        ano_atual = datetime.now().year
        choices = []
        for ano in range(ano_atual - 1, ano_atual + 5):
            choices.append((f'{ano}', f'{ano}'))
        return choices
    
    def initial_ano() -> dict[str: str]:
        ano_atual = datetime.now().year
        return {f'{ano_atual}': f'{ano_atual}'}
        
    imovel_tipo = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Tipo do imóvel'
    )
    imovel_local = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Local do imóvel'
    )
    imovel_numero = forms.CharField(
        max_length=5, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Número do imóvel'
    )
    imovel_dia_pagamento = forms.CharField(
        max_length=5, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Dia de pagar o aluguel',
    )
    imovel_valor_aluguel = forms.CharField(
        max_length=10, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Valor do aluguel'
    )
    cliente_nome = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Nome do cliente',
    )
    cliente_ci = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Comprovante de identidade do cliente',
    )
    cliente_cpf_cnpj = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='CPF/CNPJ do cliente'
    )
    cliente_estado_civil = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Estado civil do cliente'
    )
    cliente_tipo_pessoa = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Pessoa física ou jurídica',
    )
    cliente_cidade_residencia_sede = forms.CharField(
        max_length=200, 
        required=False, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Residência/Sede do cliente')
    cliente_nacionalidade = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={'readonly': 'true', 'class': 'form-control'}),
        label='Nacionalidade do cliente',
    )
    uso_imovel = forms.ChoiceField(
        required=False, 
        choices=choices_uso_imovel, 
        widget=forms.Select(attrs={'class': 'form-control input-gerar-contrato'}),
        label='Uso residencial ou comercial',
    )
    mes_inicio = forms.ChoiceField(
        required=False, 
        choices=choices_mes, 
        widget=forms.Select(attrs={'class': 'form-control input-gerar-contrato'}),
        label='Mês de início do contrato')
    ano_inicio =forms.ChoiceField(
        required=False, 
        choices=choices_ano(), 
        widget=forms.Select(attrs={'class': 'form-control input-gerar-contrato'}),
        label='Ano de início do contrato')
    mes_final = forms.ChoiceField(
        required=False, 
        choices=choices_mes, 
        widget=forms.Select(attrs={'class': 'form-control input-gerar-contrato'}),
        label='Mês final do contrato',
    )
    ano_final =forms.ChoiceField(
        required=False, 
        choices=choices_ano(), 
        widget=forms.Select(attrs={'class': 'form-control input-gerar-contrato'}),
        label='Ano final do contrato',
    )