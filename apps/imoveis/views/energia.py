from django.shortcuts import render, redirect
from ..forms import FormEnergia, FormLabel
from ..models import Energia, EnergiaLabels
from helper import verifica_autenticacao
from django.contrib import messages


def energia_lista(request):
    verifica_autenticacao(request)
    if request.method == "POST":
        if request.POST.get("id") is not None:
            try:
                id_energia = request.POST.get("id")
                energia = Energia.objects.get(id=id_energia)
                form = FormEnergia(request.POST, instance=energia)
                form.save()
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
    labels = EnergiaLabels.objects.last()
    if not labels:
        labels_dados = {
            "relogio_1": "Imovel 1",
            "relogio_2": "Imovel 2",
            "relogio_3": "Imovel 3",
        }
        labels = EnergiaLabels.objects.create(**labels_dados)
    if len(registros) > 0:
        ultimo_id = registros.last().get("id")
        if registros:
            quantidade_registros = len(registros)
            ultimos_registros = registros[
                quantidade_registros - 4 : quantidade_registros
            ]
            dados_calculados = calcula_energia(ultimos_registros)
            return render(
                request,
                "energia/energia.html",
                {
                    "registros": dados_calculados,
                    "ultimo": ultimo_id,
                    "labels": labels,
                },
            )
    return render(request, "energia/energia.html")


def energia_inserir(request):
    verifica_autenticacao(request)
    form = FormEnergia()
    return render(request, "energia/formulario.html", {"form": form})


def energia_editar(request, energia_id):
    verifica_autenticacao(request)
    registro = Energia.objects.get(id=energia_id)
    form = FormEnergia(instance=registro)
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
            "porcentagem_1": round(gasto_relogio_1 / gasto_total_kwh * 100, 2),
            "relogio_2": registro["relogio_2"],
            "energia_2": gasto_relogio_2 / gasto_total_kwh * registro["valor_conta"],
            "porcentagem_2": round(gasto_relogio_2 / gasto_total_kwh * 100, 2),
            "relogio_3": registro["relogio_3"],
            "energia_3": gasto_relogio_3 / gasto_total_kwh * registro["valor_conta"],
            "porcentagem_3": round(gasto_relogio_3 / gasto_total_kwh * 100, 2),
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


def labels_editar(request):
    verifica_autenticacao
    if request.POST:
        labels = EnergiaLabels.objects.last()
        form_labels = FormLabel(instance=labels, data=request.POST)
        if form_labels.is_valid():
            form_labels.save()
            messages.success(request, 'Novos labels salvos com sucesso')
            return redirect('energia_lista')

    labels = EnergiaLabels.objects.last()
    form_labels = FormLabel(instance=labels)
    return render(request, 'energia/labels_editar.html', {'form': form_labels})
