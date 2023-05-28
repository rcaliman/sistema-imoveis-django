import calendar
from datetime import datetime
from django.shortcuts import redirect
from num2words import num2words
from django.contrib import messages


def verifica_autenticacao(request):
    if not request.user.is_authenticated:
        if request.path != "/":
            messages.error(request, "Você não está autenticado!")
        return redirect("index")


def calcula_proxima_data(mes, ano):
    if mes in "dezembro":
        return {"mes": "janeiro", "ano": ano + 1}
    for i in range(1, 13):
        if calendar.month_name[i] == mes:
            return {"mes": calendar.month_name[i + 1], "ano": ano}


class GeraHtml:
    @staticmethod
    def select_mes():
        mes_atual = datetime.now().month
        select_mes = (
            '<select name="recibo_mes" class="inputgerarrecibo" id="recibo_mes">'
        )
        for i in range(1, 13):
            if mes_atual == i:
                select_mes += f'<option value="{calendar.month_name[i]}" selected>{calendar.month_name[i]}</option>'
            else:
                select_mes += f"<option>{calendar.month_name[i]}</option>"
        select_mes += "</select>"
        return select_mes

    @staticmethod
    def select_ano():
        ano_atual = datetime.now().year
        select_ano = (
            '<select name="recibo_ano" class="inputgerarrecibo" id="recibo_ano">'
        )
        select_ano += f'<option value="{ano_atual - 1}">{ano_atual - 1}</option>'
        select_ano += f'<option value="{ano_atual}" selected>{ano_atual}</option>'
        select_ano += f'<option value="{ano_atual + 1}">{ano_atual + 1}</option>'
        select_ano += "</select>"
        return select_ano


class Recibos:
    @staticmethod
    def gerador(registros, mes, ano):
        texto_recibo = '<div class="container-fluid">'
        conta_pagina = 1
        for registro in registros:
            if registro.__dict__["cliente_id"]:
                for i in range(0, 2):
                    valor = num2words(
                        registro.valor, to="currency", lang="pt_BR"
                    ).replace(", ", " e ")
                    if registro.tipo == "condomínio":
                        texto_recibo = Recibos.gera_recibo_de_condominio(
                            mes, ano, registro, texto_recibo, valor
                        )
                    else:
                        texto_recibo = Recibos.gera_recibo_de_aluguel(
                            mes, ano, registro, texto_recibo, valor
                        )
                    if i == 1:
                        texto_recibo += f'<p class="contapagina" style="page-break-after: always">{conta_pagina}</p>'
                        conta_pagina += 1
        return texto_recibo

    @staticmethod
    def gera_recibo_de_condominio(mes, ano, registro, texto_recibo, valor):
        data_recibo = calcula_proxima_data(mes, ano)
        texto_recibo += f"""
                            <div class='recibo'>
                                <h1 class='titulo'>RECIBO DE CONDOMÍNIO</h1>
                                <div id='linharecibo' class='linharecibo'>Recebi de <b>{registro.cliente}</b>
                                 a importância de <b>{valor}</b> 
                                 referente ao condominio do mês de <b>{mes}</b> de <b>{ano}</b>
                                 de {registro.observacao} no Edifício Caliman.
                            </div>
                            <p class='linhadata'>Colatina-ES, 1 de {data_recibo['mes']} de {data_recibo['ano']}.
                            <p class='linhaassinatura'>___________________________________
                            <br>Darci Francisco Caliman<br>Proprietário</p>
                            <p class='linhatelefone'>&nbsp; </p>
                            </div>
                            <hr style='border-top: solid 2px;'>
                        """
        texto_recibo += "</div>"
        return texto_recibo

    @staticmethod
    def gera_recibo_de_aluguel(mes, ano, registro, texto_recibo, valor):
        texto_recibo += f"""
                        <div class ='recibo'>
                            <h1 class ='titulo'>RECIBO</h1>
                            <div id='linharecibo' class ='linharecibo'>
                                Recebi de <b>{registro.cliente}</b> a importância de
                                <b>{valor}</b> referente ao aluguel do(a) <b>{registro.tipo}</b>
                                numero <b>{registro.numero}</b>.* * * * * *
                            </div>
                            <p class = 'linhadata'>Colatina-ES, {registro.dia} de {mes} de {ano}.
                            <p class = 'linhaassinatura' >___________________________________ <br>
                            Darci Francisco Caliman <br>
                            Proprietário</p>
                            <p class ='linhatelefone'>{registro.cliente.telefone_1}&nbsp;{registro.cliente.telefone_2}</p>
                        </div >
                        <hr style='border-top: solid 2px;'>
                        """
        texto_recibo += "</div>"
        return texto_recibo
