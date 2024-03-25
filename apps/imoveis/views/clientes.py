from django.shortcuts import render, redirect
from ..models import Cliente, Imovel
from ..forms import FormCliente
from helper import verifica_autenticacao
from django.contrib import messages


def clientes_lista(request):
    verifica_autenticacao(request)
    tem_cliente_para_atualizar = request.POST.get("id")
    tem_cliente_para_adicionar = request.method == "POST"
    if tem_cliente_para_atualizar:
        id_registro = request.POST.get("id")
        cliente = Cliente.objects.get(id=id_registro)
        form = FormCliente(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente atualizado com sucesso.")
        else:
            request.session['dados_formulario_cliente'] = request.POST
            return redirect('cliente_alterar', id_registro)

    else:
        if tem_cliente_para_adicionar:
            form = FormCliente(request.POST)
            if form.is_valid():
                form.save()
                dados_formulario_cliente = request.session.get('dados_formulario_cliente', None)
                if dados_formulario_cliente:
                    del(request.session['dados_formulario_cliente'])
                messages.success(request, "Novo cliente adicionado com sucesso.")
            else:
                request.session['dados_formulario_cliente'] = request.POST
                return redirect('cliente_inserir')
    todos_os_registros = Cliente.objects.order_by("nome").all() or None
    clientes_com_imoveis = Imovel.objects.all().values_list("cliente_id", flat=True)
    return render(
        request,
        "clientes/clientes.html",
        {"registros": todos_os_registros, "imoveis": clientes_com_imoveis},
    )


def cliente_inserir(request):
    verifica_autenticacao(request)
    dados_formulario_cliente = request.session.get('dados_formulario_cliente', None)
    form = FormCliente(dados_formulario_cliente)
    if dados_formulario_cliente:
        del(request.session['dados_formulario_cliente'])
    return render(request, "clientes/formulario.html", {"form": form, "id": None})


def cliente_alterar(request, id_do_registro):
    verifica_autenticacao(request)
    if request.session.get('dados_formulario_cliente'):
        form = FormCliente(request.session['dados_formulario_cliente'])
        del(request.session['dados_formulario_cliente'])
    else:
        cliente = Cliente.objects.get(id=id_do_registro)
        form = FormCliente(instance=cliente)

    return render(
        request, "clientes/formulario.html", {"form": form, "id": id_do_registro}
    )


def cliente_apagar(request, id_do_registro):
    verifica_autenticacao(request)
    try:
        Cliente.objects.get(id=id_do_registro).delete()
        messages.success(request, "Cliente apagado com sucesso")
    except:
        messages.error(request, "Erro ao tentar apagar cliente")
    return redirect(clientes_lista)
