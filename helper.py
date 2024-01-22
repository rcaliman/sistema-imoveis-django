import calendar
from django.shortcuts import redirect
from num2words import num2words
from django.contrib import messages


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


class Recibos:
    @staticmethod
    def gerador(registros, locador, mes, ano):
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
                            locador, mes, ano, registro, texto_recibo, valor
                        )
                    else:
                        texto_recibo = Recibos.gera_recibo_de_aluguel(
                            locador, mes, ano, registro, texto_recibo, valor
                        )
                    if conta_recibo == 2:
                        texto_recibo += f'<p class="cortapagina" style="page-break-after: always">{conta_pagina}</p>'
                        conta_pagina += 1
        return texto_recibo

    @staticmethod
    def gera_recibo_de_condominio(locador, mes, ano, registro, texto_recibo, valor):
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
                            <br>{locador or ''}</p>
                            <p class='linhatelefone'>&nbsp; </p>
                            </div>
                            <hr style='border-top: solid 2px;'>
                        """
        texto_recibo += "</div>"
        return texto_recibo

    @staticmethod
    def gera_recibo_de_aluguel(locador, mes, ano, registro, texto_recibo, valor):
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
                            {locador or ''} <br>
                            Locador</p>
                            <p class ='linhatelefone'>{registro.cliente.telefone_1 or ''}&nbsp;{registro.cliente.telefone_2 or ''}</p>
                        </div >
                        <hr style='border-top: solid 2px;'>
                        """
        texto_recibo += "</div>"
        return texto_recibo


def verifica_documento(numero_documento) -> dict[str, str]:
    """
    como usar:
        verifica_documento("18.781.203/0001-28")
      ou
        verifica_documento("18781203000128)
      ou
        verifica_documento("667.556.317-36")
      ou
        verifica_documento("66755631736")

    retorno em caso de documento válido:
        {'documento': 'cnpj', 'numero_limpo': '18781203000128', 'numero_formatado': '18.781.203/0001-28'}
      ou
        {'documento': 'cpf', 'numero_limpo': '66755631736', 'numero_formatado': '667.556.317.36'}

    retorno em caso de documento inválido:
        {'documento': None, 'numero_limpo': None, 'numero_formatado': None}

    """

    def limpa_numero(numero_documento):
        numero_limpo = [i for i in list(numero_documento) if i.isnumeric()]
        return numero_limpo

    def calcula_digito(
        numero_documento: list, gabarito: list, primeiro_digito: int
    ) -> int:
        primeiros_numeros = numero_documento[:-2]
        if len(gabarito) >= len(primeiros_numeros):
            if primeiro_digito != None:
                primeiros_numeros = primeiros_numeros + [primeiro_digito]
            qtd_zeros_a_adicionar_a_esquerda = len(gabarito) - len(numero_documento)
            for i in range(0, qtd_zeros_a_adicionar_a_esquerda):
                numero_documento.insert(0, "0")
            soma_com_gabarito = 0
            if len(primeiros_numeros) == len(gabarito):
                while len(primeiros_numeros) > 0:
                    soma_com_gabarito += int(primeiros_numeros.pop()) * gabarito.pop()
                return calculo(soma_com_gabarito)

    def calculo(soma):
        if 11 - (soma % 11) >= 10:
            return 0
        return 11 - (soma % 11)

    numero_documento = limpa_numero(numero_documento)
    verificador = "".join(numero_documento[-2:])

    gabarito_cpf = {
        1: [i for i in range(10, 1, -1)],
        2: [i for i in range(11, 1, -1)],
    }

    gabarito_cnpj = {
        1: [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
        2: [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
    }

    primeiro_digito_cpf = calcula_digito(numero_documento.copy(), gabarito_cpf[1], None)
    segundo_digito_cpf = calcula_digito(
        numero_documento.copy(), gabarito_cpf[2], primeiro_digito_cpf
    )

    resultado_cpf = f"{primeiro_digito_cpf}{segundo_digito_cpf}"

    tipo_documento = None
    numero_limpo = None
    numero_formatado = None

    if resultado_cpf in verificador:
        tipo_documento = "cpf"
        numero_limpo = "".join(numero_documento)
        numero_formatado = "{}.{}.{}-{}".format(
            "".join(numero_documento[:-8]),
            "".join(numero_documento[-8:-5]),
            "".join(numero_documento[-5:-2]),
            "".join(numero_documento[-2:]),
        )
    else:
        primeiro_digito_cnpj = calcula_digito(
            numero_documento.copy(), gabarito_cnpj[1], None
        )
        segundo_digito_cnpj = calcula_digito(
            numero_documento.copy(), gabarito_cnpj[2], primeiro_digito_cnpj
        )
        resultado_cnpj = f"{primeiro_digito_cnpj}{segundo_digito_cnpj}"
        if resultado_cnpj in verificador:
            tipo_documento = "cnpj"
            numero_limpo = "".join(numero_documento)
            numero_formatado = "{}.{}.{}/{}-{}".format(
                "".join(numero_documento[:-12]),
                "".join(numero_documento[-12:-9]),
                "".join(numero_documento[-9:-6]),
                "".join(numero_documento[-6:-2]),
                "".join(numero_documento[-2:]),
            )
    return {
        "documento": tipo_documento,
        "numero_limpo": numero_limpo,
        "numero_formatado": numero_formatado,
    }


def formata_telefone(telefone):
    telefone = [i for i in telefone if i.isnumeric()]
    if len(telefone) >= 8:
        if len(telefone) > 8 and telefone[-9] == "9":
            telefone_formatado = "{} {} {}-{}".format(
                "".join(telefone[:-11]),
                "".join(telefone[-11:-9]),
                "".join(telefone[-9:-4]),
                "".join(telefone[-4:]),
            )
        else:
            telefone_formatado = "{} {} {}-{}".format(
                "".join(telefone[:-10]),
                "".join(telefone[-10:-8]),
                "".join(telefone[-8:-4]),
                "".join(telefone[-4:]),
            )
        return telefone_formatado
    else:
        return "".join(telefone)
