from django.shortcuts import render, get_object_or_404
from apps.imoveis.forms import FormEnergia
from apps.imoveis.models import Energia
from helper import verifica_autenticacao
from django.contrib import messages


def energia_lista(request):
    verifica_autenticacao(request)
    if request.method == "POST":
        if request.POST.get("id") is not None:
            try:
                atualiza_registro_de_energia(request)
                messages.success(request, "Registro atualizado com sucesso.")
            except:
                messages.error(request, "Erro ao tentar atualizar registro.")
        else:
            try:
                adiciona_registro_de_energia(request)
                messages.success(request, "Novo registro adicionado com sucesso.")
            except:
                messages.error(request, "Erro ao tentar adicionar novo registro.")
    registros = Energia.objects.all().values()
    ultimo_id = registros.last()["id"]
    if registros:
        quantidade_registros = len(registros)
        ultimos_registros = registros[quantidade_registros - 4 : quantidade_registros]
        dados_calculados = calcula_energia(ultimos_registros)
        return render(
            request,
            "energia/energia.html",
            {"registros": dados_calculados, "ultimo": ultimo_id},
        )
    return render(request, "energia/energia.html")


def energia_inserir(request):
    verifica_autenticacao(request)
    form = FormEnergia()
    return render(request, "energia/formulario.html", {"form": form})


def energia_editar(request, energia_id):
    verifica_autenticacao(request)
    registro = get_object_or_404(Energia, pk=energia_id)
    form = FormEnergia(registro.__dict__)
    return render(request, "energia/formulario.html", {"form": form, "id": energia_id})


def calcula_energia(registros):
    registros_de_energia = list(registros)
    contador = 0
    resultado = []
    for registro in registros_de_energia:
        if contador >= 1:
            monta_tabela_de_consumo(registros_de_energia, contador, resultado, registro)
        contador += 1
    return resultado


def monta_tabela_de_consumo(lista_energia, contador, resultado, registro):
    anterior = lista_energia[contador - 1]
    gasto_relogio_1 = registro["relogio_1"] - anterior["relogio_1"]
    gasto_relogio_2 = registro["relogio_2"] - anterior["relogio_2"]
    gasto_relogio_3 = registro["relogio_3"] - anterior["relogio_3"]
    gasto_total_kwh = gasto_relogio_1 + gasto_relogio_2 + gasto_relogio_3
    resultado.append(
        {
            "id": registro["id"],
            "data": registro["data"],
            "relogio_1": registro["relogio_1"],
            "energia_1": gasto_relogio_1 / gasto_total_kwh * registro["valor_conta"],
            "relogio_2": registro["relogio_2"],
            "energia_2": gasto_relogio_2 / gasto_total_kwh * registro["valor_conta"],
            "relogio_3": registro["relogio_3"],
            "energia_3": gasto_relogio_3 / gasto_total_kwh * registro["valor_conta"],
            "valor_kwh": registro["valor_kwh"],
            "valor_conta": registro["valor_conta"],
        }
    )


def adiciona_registro_de_energia(request):
    verifica_autenticacao(request)
    form = FormEnergia(request.POST)
    ultimo = Energia.objects.values().last()
    atualizou_1 = float(ultimo.get("relogio_1")) != float(request.POST.get("relogio_1"))
    atualizou_2 = float(ultimo.get("relogio_2")) != float(request.POST.get("relogio_2"))
    atualizou_3 = float(ultimo.get("relogio_3")) != float(request.POST.get("relogio_3"))
    if atualizou_1 or atualizou_2 or atualizou_3 and form.is_valid:
        form.save()


def atualiza_registro_de_energia(request):
    verifica_autenticacao(request)
    id_energia = request.POST.get("id")
    energia = Energia.objects.get(pk=id_energia)
    energia.data = request.POST.get("data")
    energia.relogio_1 = request.POST.get("relogio_1")
    energia.relogio_2 = request.POST.get("relogio_2")
    energia.relogio_3 = request.POST.get("relogio_3")
    energia.valor_kwh = request.POST.get("valor_kwh")
    energia.valor_conta = request.POST.get("valor_conta")
    energia.save()
