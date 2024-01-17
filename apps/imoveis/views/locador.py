from django.shortcuts import render, redirect
from apps.imoveis.models import Locador
from apps.imoveis.forms import FormLocador
from django.contrib import messages
from helper import verifica_autenticacao


def locadores_lista(request):
    verifica_autenticacao(request)
    if request.POST:
        if request.POST.get("id") is not None:
            locador_id = request.POST.get("id")
            locador = Locador.objects.get(id=locador_id)
            form = FormLocador(request.POST, instance=locador)
            if form.is_valid():
                form.save()
                messages.success(request, "locador atualizado com sucesso")
        else:
            form = FormLocador(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "locador adicionado com sucesso")
            else:
                messages.error(request, "erro ao adicionar locador")
    todos_os_locadores = Locador.objects.all()
    return render(
        request, "locadores/locadores.html", {"registros": todos_os_locadores}
    )


def locador_inserir(request):
    verifica_autenticacao(request)
    form = FormLocador()
    return render(request, "locadores/formulario.html", {"form": form})


def locador_alterar(request, id_do_registro):
    locador = Locador.objects.get(id=id_do_registro)
    form = FormLocador(instance=locador)
    return render(
        request, "locadores/formulario.html", {"form": form, "id": id_do_registro}
    )


def locador_apagar(request, id_do_registro):
    verifica_autenticacao(request)
    locador = Locador.objects.get(id=id_do_registro)
    if locador.delete():
        messages.success(request, "locador apagado com sucesso")
    else:
        messages.error(request, "erro ao apagar locador")
    return redirect(locadores_lista)
