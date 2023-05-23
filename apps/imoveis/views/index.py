from django.shortcuts import render, redirect
from apps.imoveis.forms import FormLogin
from django.contrib.auth import authenticate, login, logout
from helper import verifica_autenticacao
from django.contrib import messages


def index(request):
    verifica_autenticacao(request)
    if request.method == "POST":
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]
        autenticacao = authenticate(request, username=usuario, password=senha)
        if autenticacao is not None:
            login(request, autenticacao)
            messages.success(request, "Usuário logado com sucesso.")
            return redirect("index")
        else:
            messages.error(
                request, "Erro ao tentar autenticar usuário, verifique sua senha."
            )
    form = FormLogin()
    return render(request, "shared/index.html", {"form": form})


def imoveis_logout(request):
    verifica_autenticacao(request)
    try:
        logout(request)
        messages.success(request, "Logout efetuado com sucesso.")
    except:
        messages.error(request, "Erro ao tentar fazer logout.")
    return redirect("index")
