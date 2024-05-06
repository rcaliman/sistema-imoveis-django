from django.shortcuts import render, redirect
from ..models import Imovel, Historico, Cliente, Contrato
from ..forms import FormImovel, FormRecibos
from helper import (
    Recibos,
    verifica_autenticacao,
    verifica_documento,
    energia_busca_contas,
)
from django.contrib import messages


def imoveis_lista(request):
    verifica_autenticacao(request)
    if request.POST.get("id") is not None:
        try:
            id_registro = request.POST.get("id")
            imovel = Imovel.objects.get(id=id_registro)
            form = FormImovel(request.POST, instance=imovel)
            if form.is_valid:
                salva_historico(form)
                form.save()
                messages.success(request, "Imóvel atualizado com sucesso.")
        except:
            messages.error(request, "Erro ao atualizar imóvel.")
    else:
        form = FormImovel(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Imóvel adicionado com sucesso.")
                salva_historico(form)
            except:
                messages.error(request, "Erro ao tentar adicionar novo imóvel")
    todos_os_registros = Imovel.objects.all()
    return render(
        request,
        "imoveis/imoveis.html",
        {
            "registros": todos_os_registros,
            "selects": FormRecibos,
        },
    )


def imovel_inserir(request):
    verifica_autenticacao(request)
    form = FormImovel()
    return render(request, "imoveis/formulario.html", {"form": form, "id": None})


def imovel_alterar(request, id_do_registro):
    verifica_autenticacao(request)
    registro = Imovel.objects.get(id=id_do_registro)
    form_do_registro = FormImovel(instance=registro)
    return render(
        request,
        "imoveis/formulario.html",
        {"form": form_do_registro, "id": id_do_registro},
    )


def imovel_apagar(request, id_do_registro):
    verifica_autenticacao(request)
    try:
        Imovel.objects.get(id=id_do_registro).delete()
        messages.success(request, "Imóvel apagado com sucesso.")
    except:
        messages.error(request, "Erro ao tentar apagar imóvel.")
    return redirect(imoveis_lista)


def imoveis_ordenados(request, ordenador):
    verifica_autenticacao(request)
    registros_ordenados = Imovel.objects.order_by(ordenador).all()
    return render(
        request,
        "imoveis/imoveis.html",
        {
            "registros": registros_ordenados,
            "selects": FormRecibos,
        },
    )


def imoveis_recibos(request):
    verifica_autenticacao(request)
    if request.method == "POST":
        id_registros = dict(request.POST.lists()).get("imprimir")
        locador, mes, ano = (
            request.POST.get("select_locador"),
            request.POST.get("select_mes"),
            request.POST.get("select_ano"),
        )
        try:
            registros_selecionados = Imovel.objects.filter(
                id__in=id_registros
            ).order_by("cliente__nome")
        except:
            messages.error(
                request, "Você não selecionou nenhum cliente para imprimir recibo."
            )
            return redirect("imoveis_lista")
        return render(
            request,
            "imoveis/recibos.html",
            {"registros": Recibos.gerador(registros_selecionados, locador, mes, ano)},
        )
    return redirect("imoveis_lista")


def historico_listar(request, imovel_id):
    verifica_autenticacao(request)
    contratos = Contrato.objects.filter(imovel__id=imovel_id).order_by("-id")
    historico = Historico.objects.filter(imovel__id=imovel_id).order_by("-id")
    imovel = Imovel.objects.get(id=imovel_id)
    try:
        cd_un_consumidora = imovel.elfsm_inscricao
        nr_cgc_cpf = verifica_documento(imovel.elfsm_titular.cpf)["numero_limpo"]
    except:
        cd_un_consumidora = None
        nr_cgc_cpf = None
    contas_energia = energia_busca_contas(cd_un_consumidora, nr_cgc_cpf)

    return render(
        request,
        "imoveis/historico_listar.html",
        {
            "contratos": contratos,
            "historico": historico,
            "contas_energia": contas_energia,
        },
    )


def salva_historico(form):
    if form["cliente"].value().isnumeric():
        cliente = Cliente.objects.get(id=form["cliente"].value())
    data_historico = {
        "tipo": form["tipo"].value(),
        "numero": form["numero"].value(),
        "local": form["local"].value() or None,
        "valor": form["valor"].value() or None,
        "complemento": form["complemento"].value() or None,
        "observacao": form["observacao"].value() or None,
        "dia": form["dia"].value() or None,
        "cliente_nome": cliente.nome or None,
        "cliente_cpf_cnpj": cliente.cpf or None,
        "imovel": form.instance or None,
    }
    Historico.objects.create(**data_historico)
