import calendar
from datetime import datetime
from django.shortcuts import redirect
from num2words import num2words
from django.contrib import messages
from apps.imoveis.models import Locatario


def verifica_autenticacao(request):
    if not request.user.is_authenticated:
        if request.path != "/":
            messages.error(request, "Você não está autenticado!")
        return redirect("index")


def calcula_proxima_data(mes, ano):
    proximo_ano = int(ano) + 1
    if mes in "dezembro":
        return {"mes": "janeiro", "ano": str(proximo_ano)}
    for i in range(1, 13):
        if calendar.month_name[i] == mes:
            return {"mes": calendar.month_name[i + 1], "ano": ano}


class GeraHtml:
    @staticmethod
    def select_locatario():
        locatarios = Locatario.objects.all().values()
        select_locatario = '<select name="recibo_locatario" class="inputgerarrecibo" id="recibo_locatario">'
        for locatario in locatarios:
            nome = locatario.get("nome")
            select_locatario += f'<option value="{nome}">{nome}</option>'
        select_locatario += "</select>"
        return select_locatario

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
    def gerador(registros, locatario, mes, ano):
        texto_recibo = '<div class="container-fluid">'
        conta_pagina = 1
        for registro in registros:
            if registro.__dict__["cliente_id"]:
                for conta_recibo in range(1, 3):
                    valor = num2words(
                        registro.valor, to="currency", lang="pt_BR"
                    ).replace(", ", " e ")

                    if registro.tipo == "condomínio":
                        texto_recibo = Recibos.gera_recibo_de_condominio(
                            locatario, mes, ano, registro, texto_recibo, valor
                        )
                    else:
                        texto_recibo = Recibos.gera_recibo_de_aluguel(
                            locatario, mes, ano, registro, texto_recibo, valor
                        )
                    if conta_recibo == 2:
                        texto_recibo += f'<p class="cortapagina" style="page-break-after: always">{conta_pagina}</p>'
                        conta_pagina += 1
        return texto_recibo

    @staticmethod
    def gera_recibo_de_condominio(locatario, mes, ano, registro, texto_recibo, valor):
        data_recibo = calcula_proxima_data(mes, ano)
        texto_recibo += f"""
                            <div class='recibo'>
                                <h1 class='titulo'>RECIBO DE CONDOMÍNIO</h1>
                                <div id='linharecibo' class='linharecibo'>Recebi de <b>{registro.cliente or ''}</b>
                                 a importância de <b>{valor or ''}</b> 
                                 referente ao condominio do mês de <b>{mes or ''}</b> de <b>{ano or ''}</b>
                                 de {registro.complemento or ''} no Edifício Caliman.
                            </div>
                            <p class='linhadata'>Colatina-ES, 1 de {data_recibo['mes'] or ''} de {data_recibo['ano'] or ''}.
                            <p class='linhaassinatura'>___________________________________
                            <br>{locatario or ''}</p>
                            <p class='linhatelefone'>&nbsp; </p>
                            </div>
                            <hr style='border-top: solid 2px;'>
                        """
        texto_recibo += "</div>"
        return texto_recibo

    @staticmethod
    def gera_recibo_de_aluguel(locatario, mes, ano, registro, texto_recibo, valor):
        complemento = ""
        if registro.complemento:
            complemento = registro.complemento + "."
        texto_recibo += f"""
                        <div class ='recibo'>
                            <h1 class ='titulo'>RECIBO</h1>
                            <div id='linharecibo' class ='linharecibo'>
                                Recebi de <b>{registro.cliente or ''}</b> a importância de
                                <b>{valor or ''}</b> referente ao aluguel do(a) <b>{registro.tipo or ''}</b>
                                numero <b>{registro.numero or ''}</b>. {complemento or ''}* * * * * *
                            </div>
                            <p class = 'linhadata'>Colatina-ES, {registro.dia or ''} de {mes or ''} de {ano or ''}.
                            <p class = 'linhaassinatura' >___________________________________ <br>
                            {locatario or ''} <br>
                            Locatário</p>
                            <p class ='linhatelefone'>{registro.cliente.telefone_1 or ''}&nbsp;{registro.cliente.telefone_2 or ''}</p>
                        </div >
                        <hr style='border-top: solid 2px;'>
                        """
        texto_recibo += "</div>"
        return texto_recibo
