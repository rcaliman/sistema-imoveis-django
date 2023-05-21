from django.shortcuts import render, redirect
from imoveis.models import Cliente
from imoveis.forms import FormCliente
from helper import verifica_autenticacao


def clientes_lista(request):
    verifica_autenticacao(request)
    if request.POST.get("id") is not None:
        atualiza_registro_de_cliente(request)
    else:
        if request.method == "POST":
            form = FormCliente(request.POST)
            if form.is_valid():
                form.save()
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
    Cliente.objects.get(pk=id_do_registro).delete()
    return redirect(clientes_lista)


def atualiza_registro_de_cliente(request):
    id_registro = request.POST.get("id")
    cliente = Cliente.objects.get(pk=id_registro)
    cliente.nome = request.POST.get("nome") or None
    cliente.data_nascimento = request.POST.get("data_nascimento") or None
    cliente.ci = request.POST.get("ci") or None
    cliente.cpf = request.POST.get("cpf") or None
    cliente.telefone_1 = request.POST.get("telefone_1") or None
    cliente.telefone_2 = request.POST.get("telefone_2") or None
    cliente.save()
