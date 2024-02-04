from django.shortcuts import render, redirect
from django.urls import reverse
from helper import verifica_autenticacao, GeraContrato
from ..forms import FormGerarContrato
from ..models import Imovel, Contrato, Historico
from django.contrib import messages
from datetime import datetime


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
    historico = Historico.objects.filter(imovel__id=imovel_id).order_by('-id')

    return render(request, "contrato/historico_listar.html", {'contratos': contratos, 'historico': historico})

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
        gera  = GeraContrato(request.POST)

        dados_contrato = {
            "registro_id": registro_id,
            "texto_locador": gera.texto_locador,
            "texto_cliente": gera.texto_cliente,
            "quantidade_meses": gera.quantidade_meses_contrato,
            "texto_uso_imovel": gera.texto_uso_imovel,
            "texto_imovel": gera.texto_imovel,
            "texto_data_inicial": gera.texto_data_inicial,
            "texto_dia_pagamento": gera.texto_dia_pagamento,
            "texto_data_final": gera.texto_data_final,
            "texto_valor": gera.texto_valor,
            "texto_quantidade_meses": gera.texto_quantidade_meses,
            "texto_data_contrato": gera.texto_data_contrato,
            "texto_assinatura_locador": gera.texto_assinatura_locador,
            "texto_assinatura_cliente": gera.texto_assinatura_cliente,
            "action": reverse("contrato_imprimir", kwargs={'registro_id': registro_id}),
        }
    return render(request, "contrato/contrato.html", dados_contrato)
