from django.shortcuts import render, redirect
from apps.imoveis.models import Locatario
from apps.imoveis.forms import FormLocatario
from django.contrib import messages
from helper import verifica_autenticacao


def locatarios_lista(request):
    verifica_autenticacao(request)
    if request.POST:
        if request.POST.get("id") is not None:
            locatario_id = request.POST.get("id")
            locatario = Locatario.objects.get(id=locatario_id)
            form = FormLocatario(request.POST, instance=locatario)
            if form.is_valid():
                form.save()
                messages.success(request, "locatário atualizado com sucesso")
        else:
            form = FormLocatario(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "locatário adicionado com sucesso")
            else:
                messages.error(request, "erro ao adicionar locatário")
    todos_os_locatarios = Locatario.objects.all()
    return render(
        request, "locatarios/locatarios.html", {"registros": todos_os_locatarios}
    )


def locatario_inserir(request):
    verifica_autenticacao(request)
    form = FormLocatario()
    return render(request, "locatarios/formulario.html", {"form": form})


def locatario_alterar(request, id_do_registro):
    locatario = Locatario.objects.get(id=id_do_registro)
    form = FormLocatario(instance=locatario)
    return render(
        request, "locatarios/formulario.html", {"form": form, "id": id_do_registro}
    )


def locatario_apagar(request, id_do_registro):
    verifica_autenticacao(request)
    locatario = Locatario.objects.get(id=id_do_registro)
    if locatario.delete():
        messages.success(request, "locatário apagado com sucesso")
    else:
        messages.error(request, "erro ao apagar locatário")
    return redirect(locatarios_lista)
