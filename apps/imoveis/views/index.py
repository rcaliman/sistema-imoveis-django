from django.shortcuts import render, redirect
from ..forms import FormLogin
from django.contrib.auth import authenticate, login, logout
from helper import verifica_autenticacao
from django.contrib import messages
from core.settings import PROD


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
    if PROD:
        return render(request, "shared/index.html", {"form": form, "ambiente": None})
    else:
        return render(request, "shared/index.html", {"form": form, "ambiente": 'ambiente de desenvolvimento'})



def imoveis_logout(request):
    verifica_autenticacao(request)
    logout(request)
    messages.success(request, "Logout efetuado com sucesso.")
    return redirect("index")
