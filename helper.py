from django.shortcuts import redirect
from django.contrib import messages
from num2words import num2words
from calendar import month_name
from datetime import datetime
from apps.imoveis.models.locador import Locador


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
        if month_name[i] == mes:
            return {"mes": month_name[i + 1], "ano": ano}

class GeraContrato:
    def __init__(self, POST):
        self.POST = POST
    
    @property
    def texto_tipo_imovel(self):
        return "residencial" if self.POST["uso_imovel"] == "residencial" else "comercial"
    
    @property
    def texto_dia_pagamento(self):
        return self.POST["imovel_dia_pagamento"]

    @property
    def texto_uso_imovel(self):
        return 'residenciais' if self.POST['uso_imovel'] == 'residencial' else 'comerciais'
    
    @property
    def texto_data_contrato(self):
        dia = self.POST["imovel_dia_pagamento"]
        mes = month_name[int(self.POST["mes_inicio"])]
        ano =  self.POST["ano_inicio"]
        return 'Colatina, {} de {} de {}.'.format(dia, mes, ano)
    
    @property
    def quantidade_meses_contrato(self):
        dt1 = datetime(
            year=int(self.POST["ano_inicio"]),
            month=int(self.POST["mes_inicio"]),
            day=int(self.POST["imovel_dia_pagamento"]),
        )
        dt2 = datetime(
            year=int(self.POST["ano_final"]),
            month=int(self.POST["mes_final"]),
            day=int(self.POST["imovel_dia_pagamento"]),
        )
        delta = dt2 - dt1
        quantidade_meses = int(delta.days / 30)
        return quantidade_meses

    @property
    def texto_quantidade_meses(self):
        quantidade_meses = self.quantidade_meses_contrato
        quantidade_meses_extenso = num2words(quantidade_meses, lang="pt_BR")
        return '{} ({}) meses '.format(quantidade_meses, quantidade_meses_extenso)

    @property
    def texto_valor(self):
        valor = self.POST["imovel_valor_aluguel"].replace(".", ",")
        valor_extenso = num2words(self.POST["imovel_valor_aluguel"], to="currency", lang="pt_BR")
        return 'R$ {} ({})'.format(valor, valor_extenso)
        
    @property
    def texto_data_inicial(self):
        dia = self.POST["imovel_dia_pagamento"].zfill(2)
        mes = self.POST["mes_inicio"]
        ano = self.POST["ano_inicio"]
        return '{}/{}/{}'.format(dia, mes, ano)
    
    @property
    def texto_data_final(self):
        dia = self.POST["imovel_dia_pagamento"].zfill(2)
        mes = self.POST["mes_final"]
        ano = self.POST["ano_final"]
        return '{}/{}/{}'.format(dia, mes, ano)

    @property
    def texto_cliente(self):
        texto_cliente = f'{self.POST["cliente_nome"].upper()}, '
        if verifica_documento(self.POST["cliente_cpf_cnpj"])["documento"] == "cpf":
            if self.POST["cliente_nacionalidade"]:
                texto_cliente += self.POST["cliente_nacionalidade"].lower() + ", "
            if self.POST["cliente_estado_civil"]:
                texto_cliente += self.POST["cliente_estado_civil"].lower() + ", "
            if self.POST["cliente_cidade_residencia_sede"]:
                texto_cliente += f'residente em {self.POST["cliente_cidade_residencia_sede"]}, '
            if self.POST["cliente_cpf_cnpj"]:
                texto_cliente += f'CPF {self.POST["cliente_cpf_cnpj"]}, '
            if self.POST["cliente_ci"]:
                texto_cliente += f'CI {self.POST["cliente_ci"]}, '
        else:
            if self.POST["cliente_cpf_cnpj"]:
                texto_cliente += f'CNPJ {self.POST["cliente_cpf_cnpj"]}, '
            if self.POST["cliente_cidade_residencia_sede"]:
                texto_cliente += f'sediado(a) em {self.POST["cliente_cidade_residencia_sede"]}, '
        return texto_cliente

    @property
    def texto_locador(self):
        locador = Locador.objects.get(id=self.POST["select_locador"])
        texto_locador = ""
        if locador.nome:
            texto_locador += locador.nome.upper() + ", "
        if locador.nacionalidade:
            texto_locador += locador.nacionalidade.lower() + ", "
        if locador.estado_civil:
            texto_locador += locador.estado_civil.lower() + ", "
        if locador.residencia:
            texto_locador += f"residente em {locador.residencia}, "
        if locador.cpf:
            texto_locador += f"CPF {locador.cpf}, "
        return texto_locador

    @property
    def texto_imovel(self):
        tipo = self.texto_tipo_imovel
        numero = int(self.POST["imovel_numero"])
        local = self.POST["imovel_local"]
        return '{} de número {} localizado na {} '.format(tipo, numero, local)

    @property
    def texto_assinatura_locador(self):
        locador = locador = Locador.objects.get(id=self.POST["select_locador"])
        return f"{locador.nome.upper()} - {locador.cpf}"
    
    @property
    def texto_assinatura_cliente(self):
        return f'{self.POST["cliente_nome"].upper()} - {self.POST["cliente_cpf_cnpj"]}'



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
