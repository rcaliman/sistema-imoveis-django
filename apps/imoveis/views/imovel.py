from django.shortcuts import render, redirect
from apps.imoveis.models import Imovel
from apps.imoveis.forms import FormImovel
from helper import GeraHtml, Recibos, verifica_autenticacao
from django.contrib import messages


def imoveis_lista(request):
    verifica_autenticacao(request)
    if request.method == "POST":
        if request.POST.get("id") is not None:
            try:
                atualiza_registro_do_imovel(request)
                messages.success(request, "Imóvel atualizado com sucesso.")
            except:
                messages.error(request, "Erro ao atualizar imóvel.")
        else:
            form = FormImovel(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Imóvel adicionado com sucesso.")
                except:
                    messages.error(request, "Erro ao tentar adicionar novo imóvel")
    todos_os_registros = Imovel.objects.all()
    return render(
        request,
        "imoveis/imoveis.html",
        {"registros": todos_os_registros, "selects": GeraHtml},
    )


def imovel_inserir(request):
    verifica_autenticacao(request)
    form = FormImovel()
    return render(request, "imoveis/formulario.html", {"form": form})


def imovel_alterar(request, id_do_registro):
    verifica_autenticacao(request)
    registro = Imovel.objects.get(id=id_do_registro)
    registro.__dict__["cliente"] = registro.__dict__.get("cliente_id")
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
    return render(request, "imoveis/imoveis.html", {"registros": registros_ordenados})


def imoveis_recibos(request):
    verifica_autenticacao(request)
    if request.method == "POST":
        id_registros = dict(request.POST.lists()).get("imprimir")
        locatario, mes, ano = (
            request.POST.get("recibo_locatario"),
            request.POST.get("recibo_mes"),
            request.POST.get("recibo_ano"),
        )
        registros_selecionados = Imovel.objects.filter(id__in=id_registros).order_by(
            "cliente__nome"
        )
        return render(
            request,
            "imoveis/recibos.html",
            {"registros": Recibos.gerador(registros_selecionados, locatario, mes, ano)},
        )
    return redirect("imoveis_lista")


def atualiza_registro_do_imovel(request):
    verifica_autenticacao(request)
    id_registro = request.POST.get("id")
    registro = Imovel.objects.get(id=id_registro)
    form = FormImovel(request.POST, instance=registro)
    form.save()
