from django.shortcuts import render, redirect
from apps.imoveis.models import Cliente
from apps.imoveis.forms import FormCliente
from helper import verifica_autenticacao
from django.contrib import messages


def clientes_lista(request):
    verifica_autenticacao(request)
    if request.POST.get("id") is not None:
        try:
            atualiza_registro_de_cliente(request)
            messages.success(request, "Cliente atualizado com sucesso.")
        except:
            messages.error(request, "Erro ao tentar atualizar cliente.")
    else:
        if request.method == "POST":
            form = FormCliente(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Novo cliente adicionado com sucesso.")
                except:
                    messages.error(request, "Erro ao tentar adicionar novo cliente.")
    todos_os_registros = Cliente.objects.order_by("nome").all()
    return render(request, "clientes/clientes.html", {"registros": todos_os_registros})


def cliente_inserir(request):
    verifica_autenticacao(request)
    form = FormCliente()
    return render(request, "clientes/formulario.html", {"form": form})


def cliente_alterar(request, id_do_registro):
    verifica_autenticacao(request)
    cliente = Cliente.objects.get(pk=id_do_registro)
    form = FormCliente(cliente.__dict__)
    return render(
        request, "clientes/formulario.html", {"form": form, "id": id_do_registro}
    )


def cliente_apagar(request, id_do_registro):
    verifica_autenticacao(request)
    try:
        Cliente.objects.get(pk=id_do_registro).delete()
        messages.success(request, "Cliente apagado com sucesso")
    except:
        messages.error(request, "Erro ao tentar apagar cliente")
    return redirect(clientes_lista)


def atualiza_registro_de_cliente(request):
    verifica_autenticacao(request)
    id_registro = request.POST.get("id")
    cliente = Cliente.objects.get(pk=id_registro)
    cliente.nome = request.POST.get("nome") or None
    cliente.data_nascimento = request.POST.get("data_nascimento") or None
    cliente.ci = request.POST.get("ci") or None
    cliente.cpf = request.POST.get("cpf") or None
    cliente.telefone_1 = request.POST.get("telefone_1") or None
    cliente.telefone_2 = request.POST.get("telefone_2") or None
    cliente.save()
