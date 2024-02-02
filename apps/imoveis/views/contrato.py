from django.shortcuts import render, redirect
from django.urls import reverse
from helper import verifica_autenticacao
from apps.imoveis.forms.contrato import FormGerarContrato
from apps.imoveis.models.imovel import Imovel
from apps.imoveis.models.locador import Locador
from apps.imoveis.models.contrato import Contrato
from django.contrib import messages
from datetime import datetime
from num2words import num2words
from calendar import month_name
from helper import verifica_documento


def contrato_form(request, registro_id):
    verifica_autenticacao(request)
    imovel = Imovel.objects.get(id=registro_id)
    if not (imovel.cliente.cpf):
        messages.error(
            request,
            "Cliente sem CPF ou CNPJ cadastrado, entre em Clientes e faça o cadastro.",
        )
        return redirect("imoveis_lista")
    dados_form = {
        "imovel_tipo": imovel.tipo,
        "imovel_local": imovel.local,
        "imovel_numero": imovel.numero,
        "imovel_dia_pagamento": imovel.dia,
        "imovel_valor_aluguel": imovel.valor,
        "cliente_nome": imovel.cliente.nome,
        "cliente_ci": imovel.cliente.ci,
        "cliente_cpf_cnpj": imovel.cliente.cpf,
        "cliente_estado_civil": imovel.cliente.estado_civil,
        "cliente_cidade_residencia_sede": imovel.cliente.cidade_residencia_sede,
        "cliente_nacionalidade": imovel.cliente.nacionalidade,
        "mes_inicio": (datetime.now().month, datetime.now().month),
        "ano_inicio": (datetime.now().year, datetime.now().year),
        "mes_final": (datetime.now().month, datetime.now().month),
        "ano_final": (datetime.now().year, datetime.now().year),
    }
    form = FormGerarContrato(dados_form)

    return render(
        request,
        "contrato/contrato_form.html",
        {"form": form, "registro_id": registro_id},
    )

def contratos_listar(request, imovel_id):
    verifica_autenticacao(request)
    contratos = Contrato.objects.filter(imovel__id=imovel_id).order_by('-id')

    return render(request, "contrato/contratos_listar.html", {'contratos': contratos})

def contrato_imprimir(request, registro_id):
    verifica_autenticacao(request)
    if request.POST:
        texto_pagina = request.POST.get("texto_pagina")
        salvar_contrato = request.POST.get("salvar_contrato")

        contrato = {
            "imovel": Imovel.objects.get(id=registro_id),
            "texto": texto_pagina,
        }
        if salvar_contrato is not None:
            Contrato.objects.create(**contrato)
        script = 'window.print()'
    else:
        texto_pagina = Contrato.objects.filter(id=registro_id)[0].texto
        script = ''

    return render(request, "contrato/contrato_imprimir.html", {"texto": texto_pagina, 'script': script})


def contrato(request, registro_id):
    verifica_autenticacao(request)
    if request.POST:
        POST = request.POST
        quantidade_meses = calcula_quantidade_meses_contrato(POST)
        texto_locador = gera_texto_locador(POST)
        texto_cliente = gera_texto_cliente(POST)
        texto_uso_imovel = (
            "residenciais" if POST["uso_imovel"] == "residencial" else "comerciais"
        )
        tipo_imovel = (
            "residencial" if POST["uso_imovel"] == "residencial" else "comercial"
        )
        texto_imovel = f'{tipo_imovel} de número {POST["imovel_numero"]} localizado na {POST["imovel_local"]} '
        texto_data_inicial = gera_texto_data_inicial(POST)
        texto_dia_pagamento = POST["imovel_dia_pagamento"]
        texto_data_final = gera_texto_data_final(POST)
        texto_valor = gera_texto_valor(POST)
        texto_quantidade_meses = gera_texto_quantidade_meses(quantidade_meses)
        texto_data_contrato = gera_texto_data_contrato(POST)
        texto_assinatura_locador = gera_texto_assinatura_locador(POST)
        texto_assinatura_cliente = (
            f'{POST["cliente_nome"].upper()} - {POST["cliente_cpf_cnpj"]}'
        )
        dados_contrato = {
            "registro_id": registro_id,
            "quantidade_meses": quantidade_meses,
            "texto_locador": texto_locador,
            "texto_cliente": texto_cliente,
            "texto_uso_imovel": texto_uso_imovel,
            "texto_imovel": texto_imovel,
            "texto_data_inicial": texto_data_inicial,
            "texto_dia_pagamento": texto_dia_pagamento,
            "texto_data_final": texto_data_final,
            "texto_valor": texto_valor,
            "texto_quantidade_meses": texto_quantidade_meses,
            "texto_data_contrato": texto_data_contrato,
            "texto_assinatura_locador": texto_assinatura_locador,
            "texto_assinatura_cliente": texto_assinatura_cliente,
            "action": reverse("contrato_imprimir", kwargs={'registro_id': registro_id}),
        }
    return render(request, "contrato/contrato.html", dados_contrato)


def gera_texto_data_contrato(POST):
    return f'Colatina, {POST["imovel_dia_pagamento"]} de {month_name[int(POST["mes_inicio"])]} de {POST["ano_inicio"]}.'


def gera_texto_quantidade_meses(quantidade_meses):
    return f'{quantidade_meses} ({num2words(quantidade_meses, lang="pt_BR")}) meses '


def gera_texto_valor(POST):
    return f'R$ {POST["imovel_valor_aluguel"]} ({num2words(POST["imovel_valor_aluguel"], to="currency", lang="pt_BR")})'.replace(
        ".", ","
    )


def gera_texto_data_final(POST):
    return f'{POST["imovel_dia_pagamento"].zfill(2)}/{POST["mes_final"]}/{POST["ano_final"]}'


def gera_texto_data_inicial(POST):
    return f'{POST["imovel_dia_pagamento"].zfill(2)}/{POST["mes_inicio"]}/{POST["ano_inicio"]}'


def calcula_quantidade_meses_contrato(POST):
    dt1 = datetime(
        year=int(POST["ano_inicio"]),
        month=int(POST["mes_inicio"]),
        day=int(POST["imovel_dia_pagamento"]),
    )
    dt2 = datetime(
        year=int(POST["ano_final"]),
        month=int(POST["mes_final"]),
        day=int(POST["imovel_dia_pagamento"]),
    )
    delta = dt2 - dt1
    quantidade_meses = int(delta.days / 30)
    return quantidade_meses


def gera_texto_cliente(POST):
    texto_cliente = f'{POST["cliente_nome"].upper()}, '
    if verifica_documento(POST["cliente_cpf_cnpj"])["documento"] == "cpf":
        if POST["cliente_nacionalidade"]:
            texto_cliente += POST["cliente_nacionalidade"].lower() + ", "
        if POST["cliente_estado_civil"]:
            texto_cliente += POST["cliente_estado_civil"].lower() + ", "
        if POST["cliente_cidade_residencia_sede"]:
            texto_cliente += f'residente em {POST["cliente_cidade_residencia_sede"]}, '
        if POST["cliente_cpf_cnpj"]:
            texto_cliente += f'CPF {POST["cliente_cpf_cnpj"]}, '
        if POST["cliente_ci"]:
            texto_cliente += f'CI {POST["cliente_ci"]}, '
    else:
        if POST["cliente_cpf_cnpj"]:
            texto_cliente += f'CNPJ {POST["cliente_cpf_cnpj"]}, '
        if POST["cliente_cidade_residencia_sede"]:
            texto_cliente += f'sediado(a) em {POST["cliente_cidade_residencia_sede"]}, '
    return texto_cliente


def gera_texto_locador(POST):
    locador = Locador.objects.get(id=POST["select_locador"])
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


def gera_texto_assinatura_locador(POST):
    locador = locador = Locador.objects.get(id=POST["select_locador"])
    return f"{locador.nome.upper()} - {locador.cpf}"
