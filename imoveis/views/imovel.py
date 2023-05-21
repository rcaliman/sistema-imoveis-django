from django.shortcuts import render, redirect
from imoveis.models import Imovel, Cliente
from imoveis.forms import FormImovel
from helper import ComponentesHtml, Recibos


def imoveis_lista(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        if request.POST.get("id") is not None:
            atualiza_registro_do_imovel(request)
        else:
            form = FormImovel(request.POST)
            if form.is_valid():
                form.save()
    todos_os_registros = Imovel.objects.all()
    return render(
        request,
        "imoveis/imoveis.html",
        {"registros": todos_os_registros, "selects": ComponentesHtml},
    )


def imovel_inserir(request):
    if not request.user.is_authenticated:
        return redirect("index")
    form = FormImovel()
    return render(request, "imoveis/formulario.html", {"form": form})


def imovel_alterar(request, id_do_registro):
    if not request.user.is_authenticated:
        return redirect("index")
    registro = Imovel.objects.get(pk=id_do_registro)
    registro.__dict__["cliente"] = registro.__dict__["cliente_id"]
    form_do_registro = FormImovel(registro.__dict__)
    return render(
        request,
        "imoveis/formulario.html",
        {"form": form_do_registro, "id": id_do_registro},
    )


def imovel_apagar(request, id_do_registro):
    if not request.user.is_authenticated:
        return redirect("index")
    Imovel.objects.get(pk=id_do_registro).delete()
    return redirect(imoveis_lista)


def imoveis_ordenados(request, ordenador):
    if not request.user.is_authenticated:
        return redirect("index")
    registros_ordenados = Imovel.objects.order_by(ordenador).all()
    return render(request, "imoveis/imoveis.html", {"registros": registros_ordenados})


def imoveis_recibos(request):
    if not request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        id_registros = dict(request.POST.lists()).get("imprimir")
        mes, ano = request.POST["recibo_mes"], request.POST["recibo_ano"]
        registros_selecionados = Imovel.objects.filter(id__in=id_registros).order_by(
            "cliente__nome"
        )
        return render(
            request,
            "imoveis/recibos.html",
            {"registros": Recibos.gerador(registros_selecionados, mes, ano)},
        )
    return redirect("imoveis_lista")


def atualiza_registro_do_imovel(request):
    id_registro = request.POST.get("id")
    registro = Imovel.objects.get(pk=id_registro)
    registro.tipo = request.POST.get("tipo") or None
    registro.numero = request.POST.get("numero") or None
    registro.local = request.POST.get("local") or None
    registro.cliente = Cliente(request.POST.get("cliente")) or None
    registro.valor = request.POST.get("valor") or None
    registro.observacao = request.POST.get("observacao") or None
    registro.dia = request.POST.get("dia") or None
    registro.save()
